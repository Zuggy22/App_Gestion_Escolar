from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Planificacion, MensajeAlumno
from .forms import PlanificacionForm, MensajeAlumnoForm
from profesores.models import Profesor
from alumnos.models import Alumno


# ── Helpers ──────────────────────────────────────────────────
def get_profesores(request):
    return Profesor.objects.all().order_by('nombre')


# ══════════════════════════════════════════
#   PLANIFICACIONES
# ══════════════════════════════════════════

@login_required
def lista_planificaciones(request):
    prof_id   = request.GET.get('profesor', '')
    tipo_fil  = request.GET.get('tipo', '')
    curso_fil = request.GET.get('curso', '')

    planificaciones = Planificacion.objects.select_related('profesor').all()

    if prof_id:
        planificaciones = planificaciones.filter(profesor__pk=prof_id)
    if tipo_fil:
        planificaciones = planificaciones.filter(tipo=tipo_fil)
    if curso_fil:
        planificaciones = planificaciones.filter(curso=curso_fil)

    cursos = Planificacion.objects.values_list('curso', flat=True).distinct().order_by('curso')

    return render(request, 'planificaciones/lista.html', {
        'planificaciones': planificaciones,
        'profesores':      get_profesores(request),
        'cursos':          cursos,
        'prof_id':         prof_id,
        'tipo_fil':        tipo_fil,
        'curso_fil':       curso_fil,
        'total':           planificaciones.count(),
    })


@login_required
def crear_planificacion(request):
    prof_id = request.GET.get('profesor', '') or request.POST.get('profesor_id', '')

    if request.method == 'POST':
        form = PlanificacionForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            try:
                plan.profesor = Profesor.objects.get(pk=request.POST.get('profesor_id'))
            except Profesor.DoesNotExist:
                messages.error(request, 'Selecciona un profesor válido.')
                return render(request, 'planificaciones/form.html', {
                    'form': form, 'profesores': get_profesores(request), 'accion': 'Crear'
                })
            plan.save()
            messages.success(request, f'✅ Planificación "{plan.unidad_tema}" creada exitosamente.')
            return redirect('planificaciones:lista')
    else:
        form = PlanificacionForm()

    return render(request, 'planificaciones/form.html', {
        'form':       form,
        'profesores': get_profesores(request),
        'prof_id':    prof_id,
        'accion':     'Crear',
    })


@login_required
def editar_planificacion(request, pk):
    plan = get_object_or_404(Planificacion, pk=pk)

    if request.method == 'POST':
        form = PlanificacionForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Planificación actualizada.')
            return redirect('planificaciones:detalle', pk=plan.pk)
    else:
        form = PlanificacionForm(instance=plan)

    return render(request, 'planificaciones/form.html', {
        'form':       form,
        'profesores': get_profesores(request),
        'prof_id':    str(plan.profesor.pk),
        'plan':       plan,
        'accion':     'Editar',
    })


@login_required
def detalle_planificacion(request, pk):
    plan = get_object_or_404(Planificacion, pk=pk)
    return render(request, 'planificaciones/detalle.html', {'plan': plan})


@login_required
def eliminar_planificacion(request, pk):
    plan = get_object_or_404(Planificacion, pk=pk)
    if request.method == 'POST':
        plan.delete()
        messages.success(request, '🗑️ Planificación eliminada.')
        return redirect('planificaciones:lista')
    return render(request, 'planificaciones/confirmar_eliminar.html', {'plan': plan})


# ══════════════════════════════════════════
#   MENSAJES A ALUMNOS
# ══════════════════════════════════════════

@login_required
def enviar_mensaje_alumnos(request):
    prof_id = request.GET.get('profesor', '') or request.POST.get('profesor_id', '')

    if request.method == 'POST':
        form = MensajeAlumnoForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            try:
                msg.profesor = Profesor.objects.get(pk=request.POST.get('profesor_id'))
            except Profesor.DoesNotExist:
                messages.error(request, 'Selecciona un profesor válido.')
                return render(request, 'planificaciones/mensaje_form.html', {
                    'form': form, 'profesores': get_profesores(request)
                })
            msg.save()

            # Determinar destinatarios
            curso = msg.curso.strip().upper()
            if curso == 'TODOS':
                alumnos = Alumno.objects.all()
            else:
                alumnos = Alumno.objects.filter(curso=msg.curso)

            msg.destinatarios.set(alumnos)

            # Enviar correos
            correos = [a.correo for a in alumnos if a.correo]
            enviados = 0
            if correos:
                for correo in correos:
                    try:
                        send_mail(
                            subject=f'[Liceo] {msg.asunto}',
                            message=(
                                f'Estimado/a alumno/a,\n\n'
                                f'{msg.mensaje}\n\n'
                                f'{"📅 Fecha importante: " + str(msg.fecha_evento.strftime("%d/%m/%Y")) if msg.fecha_evento else ""}\n\n'
                                f'Profesor/a: {msg.profesor.nombre}\n'
                                f'Asignatura: {msg.profesor.especialidad}\n\n'
                                f'— Liceo Municipal · Sistema de Gestión Escolar'
                            ),
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=[correo],
                            fail_silently=True,
                        )
                        enviados += 1
                    except Exception:
                        pass
                msg.enviado_correo = True
                msg.save()

            messages.success(
                request,
                f'✅ Mensaje enviado a {alumnos.count()} alumno(s). '
                f'Correos enviados: {enviados}.'
            )
            return redirect('planificaciones:bandeja_mensajes')
    else:
        form = MensajeAlumnoForm()

    return render(request, 'planificaciones/mensaje_form.html', {
        'form':       form,
        'profesores': get_profesores(request),
        'prof_id':    prof_id,
    })


@login_required
def bandeja_mensajes_alumnos(request):
    prof_id = request.GET.get('profesor', '')
    mensajes = MensajeAlumno.objects.select_related('profesor').prefetch_related('destinatarios')
    if prof_id:
        mensajes = mensajes.filter(profesor__pk=prof_id)
    return render(request, 'planificaciones/bandeja_mensajes.html', {
        'mensajes':   mensajes,
        'profesores': get_profesores(request),
        'prof_id':    prof_id,
        'total':      mensajes.count(),
    })
