from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import Apoderado, MensajeApoderado
from .forms  import ApoderadoForm, MensajeForm, RespuestaForm
from alumnos.models import Alumno
import datetime


@login_required
def lista_apoderados(request):
    q = request.GET.get('q', '')
    apoderados = Apoderado.objects.select_related('alumno').all()
    if q:
        apoderados = apoderados.filter(
            nombre__icontains=q
        ) | apoderados.filter(
            alumno__nombre__icontains=q
        ) | apoderados.filter(
            alumno__apellido__icontains=q
        )
    return render(request, 'apoderados/lista_apoderados.html', {
        'apoderados': apoderados,
        'busqueda':   q,
    })


@login_required
def crear_apoderado(request):
    if request.method == 'POST':
        form = ApoderadoForm(request.POST)
        if form.is_valid():
            apoderado = form.save()
            messages.success(request,
                f'✅ Apoderado {apoderado.nombre} registrado exitosamente.')
            return redirect('apoderados:detalle', pk=apoderado.pk)
    else:
        form = ApoderadoForm()
    return render(request, 'apoderados/crear_apoderado.html', {'form': form})


@login_required
def detalle_apoderado(request, pk):
    apoderado = get_object_or_404(Apoderado, pk=pk)
    mensajes  = MensajeApoderado.objects.filter(apoderado=apoderado)
    pendientes = mensajes.filter(estado='pendiente').count()

    # Informe del alumno
    from notas.models import Nota, Asistencia, ASIGNATURAS
    alumno    = apoderado.alumno
    notas_qs  = Nota.objects.filter(alumno=alumno)
    asignaturas = [a[0] for a in ASIGNATURAS]
    resumen   = []
    for asig in asignaturas:
        nota_obj   = notas_qs.filter(asignatura=asig).first()
        asist      = Asistencia.porcentaje_asistencia(alumno, asig)
        promedio   = nota_obj.promedio_asignatura() if nota_obj else None
        aprobacion = Asistencia.estado_aprobacion(asist['porcentaje'], promedio)
        resumen.append({
            'asignatura': asig,
            'promedio':   promedio,
            'porcentaje': asist['porcentaje'],
            'aprobacion': aprobacion,
        })
    promedios_v  = [r['promedio'] for r in resumen if r['promedio']]
    promedio_final = round(
        sum(promedios_v) / len(promedios_v), 1
    ) if promedios_v else None

    return render(request, 'apoderados/detalle_apoderado.html', {
        'apoderado':     apoderado,
        'mensajes':      mensajes,
        'pendientes':    pendientes,
        'resumen':       resumen,
        'promedio_final': promedio_final,
        'fecha_hoy':     datetime.date.today(),
    })


@login_required
def editar_apoderado(request, pk):
    apoderado = get_object_or_404(Apoderado, pk=pk)
    if request.method == 'POST':
        form = ApoderadoForm(request.POST, instance=apoderado)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Datos actualizados correctamente.')
            return redirect('apoderados:detalle', pk=apoderado.pk)
    else:
        form = ApoderadoForm(instance=apoderado)
    return render(request, 'apoderados/crear_apoderado.html', {
        'form': form, 'editando': True, 'apoderado': apoderado
    })


@login_required
def eliminar_apoderado(request, pk):
    apoderado = get_object_or_404(Apoderado, pk=pk)
    if request.method == 'POST':
        nombre = apoderado.nombre
        apoderado.delete()
        messages.success(request, f'🗑️ Apoderado {nombre} eliminado.')
        return redirect('apoderados:lista')
    return render(request, 'apoderados/confirmar_eliminar.html',
                  {'objeto': apoderado})


@login_required
def enviar_mensaje(request, apoderado_pk):
    """Apoderado envía mensaje al profesor jefe."""
    apoderado = get_object_or_404(Apoderado, pk=apoderado_pk)
    if request.method == 'POST':
        form = MensajeForm(request.POST)
        if form.is_valid():
            msg           = form.save(commit=False)
            msg.apoderado = apoderado
            msg.save()

            # Obtener correo del profesor jefe
            profesor = None
            if apoderado.alumno.curso:
                from cursos.models import Curso
                curso_obj = Curso.objects.filter(
                    nombre_ramo=apoderado.alumno.curso
                ).first()
                if curso_obj and curso_obj.profesor_jefe:
                    profesor = curso_obj.profesor_jefe

            # Enviar correo de notificación
            try:
                destinatario = profesor.correo if profesor and hasattr(
                    profesor, 'correo') else settings.EMAIL_HOST_USER
                send_mail(
                    subject=f'[Liceo Municipal] Mensaje de apoderado — {msg.asunto}',
                    message=f"""
Estimado/a Profesor/a,

El apoderado {apoderado.nombre} ({apoderado.get_relacion_display()} de {apoderado.alumno})
le ha enviado un mensaje a través del Sistema de Gestión Escolar.

CATEGORÍA: {msg.get_categoria_display()}
ASUNTO: {msg.asunto}

MENSAJE:
{msg.mensaje}

---
Responda desde el Sistema de Gestión Escolar:
http://127.0.0.1:8000/apoderados/mensaje/{msg.pk}/responder/

Sistema de Gestión Escolar · Liceo Municipal
                    """,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[destinatario],
                    fail_silently=True,
                )
            except Exception:
                pass  # El mensaje se guarda aunque falle el correo

            messages.success(request,
                '✅ Mensaje enviado correctamente. El profesor jefe ha sido notificado.')
            return redirect('apoderados:detalle', pk=apoderado_pk)
    else:
        form = MensajeForm()
    return render(request, 'apoderados/enviar_mensaje.html', {
        'form': form, 'apoderado': apoderado
    })


@login_required
def responder_mensaje(request, msg_pk):
    """Profesor responde un mensaje de apoderado."""
    msg = get_object_or_404(MensajeApoderado, pk=msg_pk)
    if request.method == 'POST':
        form = RespuestaForm(request.POST, instance=msg)
        if form.is_valid():
            respuesta       = form.save(commit=False)
            respuesta.fecha_respuesta = timezone.now()
            respuesta.save()

            # Notificar al apoderado por correo
            try:
                send_mail(
                    subject=f'[Liceo Municipal] Respuesta a su mensaje — {msg.asunto}',
                    message=f"""
Estimado/a {msg.apoderado.nombre},

Su mensaje ha sido respondido por el equipo docente del Liceo Municipal.

SU MENSAJE:
{msg.mensaje}

RESPUESTA:
{msg.respuesta}

Estado: {msg.get_estado_display()}

---
Sistema de Gestión Escolar · Liceo Municipal
                    """,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[msg.apoderado.correo],
                    fail_silently=True,
                )
            except Exception:
                pass

            messages.success(request, '✅ Respuesta enviada al apoderado.')
            return redirect('apoderados:bandeja')
    else:
        form = RespuestaForm(instance=msg)
    return render(request, 'apoderados/responder_mensaje.html', {
        'form': form, 'mensaje': msg
    })


@login_required
def bandeja_mensajes(request):
    """Bandeja de entrada de todos los mensajes."""
    filtro    = request.GET.get('filtro', 'todos')
    mensajes  = MensajeApoderado.objects.select_related('apoderado').all()
    if filtro == 'pendiente':
        mensajes = mensajes.filter(estado='pendiente')
    elif filtro == 'respondido':
        mensajes = mensajes.filter(estado='respondido')
    elif filtro == 'cerrado':
        mensajes = mensajes.filter(estado='cerrado')
    return render(request, 'apoderados/bandeja_mensajes.html', {
        'mensajes':   mensajes,
        'filtro':     filtro,
        'pendientes': MensajeApoderado.objects.filter(estado='pendiente').count(),
    })