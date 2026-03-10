from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
from .models import RegistroPIE, Especialista, PACI, EvaluacionPIE, InformeAvance
from .forms import (RegistroPIEForm, EspecialistaForm,
                    PACIForm, EvaluacionPIEForm, InformeAvanceForm)


# ══════════════════════════════
#  REGISTRO PIE
# ══════════════════════════════

@login_required
def lista_pie(request):
    nec_fil  = request.GET.get('necesidad', '')
    niv_fil  = request.GET.get('nivel', '')
    registros = RegistroPIE.objects.select_related('alumno').prefetch_related('especialistas')
    if nec_fil:
        registros = registros.filter(necesidad=nec_fil)
    if niv_fil:
        registros = registros.filter(nivel_apoyo=niv_fil)
    from .models import NECESIDADES, NIVELES_APOYO
    return render(request, 'pie/lista.html', {
        'registros':   registros,
        'total':       registros.count(),
        'necesidades': NECESIDADES,
        'niveles':     NIVELES_APOYO,
        'nec_fil':     nec_fil,
        'niv_fil':     niv_fil,
    })


@login_required
def crear_registro(request):
    if request.method == 'POST':
        form = RegistroPIEForm(request.POST)
        if form.is_valid():
            reg = form.save()
            messages.success(request, f'✅ Alumno {reg.alumno} ingresado al PIE.')
            return redirect('pie:detalle', pk=reg.pk)
    else:
        form = RegistroPIEForm()
    return render(request, 'pie/form_registro.html', {'form': form, 'accion': 'Ingresar'})


@login_required
def editar_registro(request, pk):
    reg = get_object_or_404(RegistroPIE, pk=pk)
    if request.method == 'POST':
        form = RegistroPIEForm(request.POST, instance=reg)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Registro actualizado.')
            return redirect('pie:detalle', pk=reg.pk)
    else:
        form = RegistroPIEForm(instance=reg)
    return render(request, 'pie/form_registro.html', {'form': form, 'accion': 'Editar', 'reg': reg})


@login_required
def detalle_pie(request, pk):
    reg          = get_object_or_404(RegistroPIE, pk=pk)
    especialistas = reg.especialistas.all()
    pacis         = reg.pacis.all()
    evaluaciones  = reg.evaluaciones.all()
    informes      = reg.informes.all()
    return render(request, 'pie/detalle.html', {
        'reg':          reg,
        'especialistas': especialistas,
        'pacis':         pacis,
        'evaluaciones':  evaluaciones,
        'informes':      informes,
    })


# ══════════════════════════════
#  ESPECIALISTAS
# ══════════════════════════════

@login_required
def agregar_especialista(request, reg_pk):
    reg = get_object_or_404(RegistroPIE, pk=reg_pk)
    if request.method == 'POST':
        form = EspecialistaForm(request.POST)
        if form.is_valid():
            esp = form.save(commit=False)
            esp.registro = reg
            esp.save()
            messages.success(request, f'✅ Especialista {esp.nombre} agregado.')
            return redirect('pie:detalle', pk=reg.pk)
    else:
        form = EspecialistaForm()
    return render(request, 'pie/form_especialista.html', {
        'form': form, 'reg': reg, 'accion': 'Agregar'
    })


@login_required
def eliminar_especialista(request, pk):
    esp = get_object_or_404(Especialista, pk=pk)
    reg_pk = esp.registro.pk
    if request.method == 'POST':
        esp.delete()
        messages.success(request, '🗑️ Especialista eliminado.')
    return redirect('pie:detalle', pk=reg_pk)


# ══════════════════════════════
#  PACI
# ══════════════════════════════

@login_required
def agregar_paci(request, reg_pk):
    reg = get_object_or_404(RegistroPIE, pk=reg_pk)
    if request.method == 'POST':
        form = PACIForm(request.POST)
        if form.is_valid():
            paci = form.save(commit=False)
            paci.registro = reg
            paci.save()
            messages.success(request, '✅ PACI creado.')
            return redirect('pie:detalle', pk=reg.pk)
    else:
        form = PACIForm(initial={'anno': timezone.now().year})
    return render(request, 'pie/form_paci.html', {
        'form': form, 'reg': reg, 'accion': 'Crear'
    })


@login_required
def editar_paci(request, pk):
    paci = get_object_or_404(PACI, pk=pk)
    if request.method == 'POST':
        form = PACIForm(request.POST, instance=paci)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ PACI actualizado.')
            return redirect('pie:detalle', pk=paci.registro.pk)
    else:
        form = PACIForm(instance=paci)
    return render(request, 'pie/form_paci.html', {
        'form': form, 'reg': paci.registro, 'paci': paci, 'accion': 'Editar'
    })


@login_required
def paci_pdf(request, pk):
    paci = get_object_or_404(PACI, pk=pk)
    reg  = paci.registro
    _generar_paci_pdf(paci, reg)
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from io import BytesIO

    buffer = BytesIO()
    p      = canvas.Canvas(buffer, pagesize=letter)
    ancho, alto = letter

    # Encabezado
    p.setFillColor(colors.HexColor('#0a1628'))
    p.rect(0, alto - 90, ancho, 90, fill=True, stroke=False)
    p.setFillColor(colors.HexColor('#f4c842'))
    p.setFont('Helvetica-Bold', 18)
    p.drawCentredString(ancho / 2, alto - 40, 'LICEO MUNICIPAL')
    p.setFont('Helvetica', 11)
    p.drawCentredString(ancho / 2, alto - 58, 'Plan de Adecuación Curricular Individual (PACI)')
    p.setFillColor(colors.HexColor('#94a3b8'))
    p.setFont('Helvetica', 9)
    p.drawCentredString(ancho / 2, alto - 74, f'Año {paci.anno} — {paci.get_trimestre_display()}')

    # Datos del alumno
    y = alto - 120
    p.setFillColor(colors.HexColor('#1e293b'))
    p.rect(40, y - 60, ancho - 80, 70, fill=True, stroke=False)
    p.setFillColor(colors.HexColor('#f4c842'))
    p.setFont('Helvetica-Bold', 9)
    p.drawString(55, y - 10, 'ALUMNO')
    p.setFillColor(colors.white)
    p.setFont('Helvetica-Bold', 12)
    p.drawString(55, y - 26, f'{reg.alumno.nombre} {reg.alumno.apellido}')
    p.setFont('Helvetica', 10)
    p.setFillColor(colors.HexColor('#94a3b8'))
    p.drawString(55, y - 42,
        f'Curso: {reg.alumno.curso}   |   '
        f'Necesidad: {reg.get_necesidad_display()}   |   '
        f'Nivel: {reg.get_nivel_apoyo_display()}')
    p.setFillColor(colors.HexColor('#94a3b8'))
    p.drawString(55, y - 56, f'Responsable PACI: {paci.responsable}   |   Asignatura: {paci.asignatura}')

    def seccion(titulo, contenido, y_pos):
        p.setFillColor(colors.HexColor('#0f172a'))
        p.rect(40, y_pos - 18, ancho - 80, 20, fill=True, stroke=False)
        p.setFillColor(colors.HexColor('#f4c842'))
        p.setFont('Helvetica-Bold', 9)
        p.drawString(50, y_pos - 10, titulo.upper())
        p.setFillColor(colors.HexColor('#1e293b'))
        lineas = _wrap_text(contenido, 90)
        altura = len(lineas) * 14 + 12
        p.rect(40, y_pos - 18 - altura, ancho - 80, altura, fill=True, stroke=False)
        p.setFillColor(colors.HexColor('#cbd5e1'))
        p.setFont('Helvetica', 9)
        yy = y_pos - 30
        for linea in lineas:
            p.drawString(50, yy, linea)
            yy -= 14
        return y_pos - 18 - altura - 10

    y = alto - 210
    y = seccion('🎯 Objetivo General',        paci.objetivo_general,      y)
    y = seccion('📌 Objetivos Específicos',    paci.objetivos_especificos, y)
    y = seccion('⚙️ Estrategias Metodológicas', paci.estrategias,          y)
    if paci.recursos:
        y = seccion('📦 Recursos y Materiales', paci.recursos,             y)

    # Firma
    y -= 20
    p.setStrokeColor(colors.HexColor('#334155'))
    p.line(55, y, 240, y)
    p.line(ancho - 240, y, ancho - 55, y)
    p.setFillColor(colors.HexColor('#64748b'))
    p.setFont('Helvetica', 8)
    p.drawCentredString(147, y - 12, 'Especialista responsable')
    p.drawCentredString(ancho - 147, y - 12, 'Director/a del establecimiento')

    p.showPage()
    p.save()
    buffer.seek(0)
    nombre = f'PACI_{reg.alumno.apellido}_{paci.anno}_T{paci.trimestre}.pdf'
    resp   = HttpResponse(buffer, content_type='application/pdf')
    resp['Content-Disposition'] = f'attachment; filename="{nombre}"'
    return resp


def _wrap_text(texto, max_chars):
    palabras = texto.replace('\n', ' \n ').split(' ')
    lineas, linea_actual = [], ''
    for p in palabras:
        if p == '\n':
            lineas.append(linea_actual)
            linea_actual = ''
        elif len(linea_actual) + len(p) + 1 <= max_chars:
            linea_actual += (' ' if linea_actual else '') + p
        else:
            if linea_actual:
                lineas.append(linea_actual)
            linea_actual = p
    if linea_actual:
        lineas.append(linea_actual)
    return lineas


def _generar_paci_pdf(paci, reg):
    pass


# ══════════════════════════════
#  EVALUACIONES PIE
# ══════════════════════════════

@login_required
def agregar_evaluacion(request, reg_pk):
    reg = get_object_or_404(RegistroPIE, pk=reg_pk)
    if request.method == 'POST':
        form = EvaluacionPIEForm(request.POST)
        form.fields['especialista'].queryset = reg.especialistas.all()
        if form.is_valid():
            ev = form.save(commit=False)
            ev.registro = reg
            ev.save()
            messages.success(request, '✅ Evaluación registrada.')
            return redirect('pie:detalle', pk=reg.pk)
    else:
        form = EvaluacionPIEForm()
        form.fields['especialista'].queryset = reg.especialistas.all()
    return render(request, 'pie/form_evaluacion.html', {
        'form': form, 'reg': reg, 'accion': 'Registrar'
    })


@login_required
def editar_evaluacion(request, pk):
    ev  = get_object_or_404(EvaluacionPIE, pk=pk)
    reg = ev.registro
    if request.method == 'POST':
        form = EvaluacionPIEForm(request.POST, instance=ev)
        form.fields['especialista'].queryset = reg.especialistas.all()
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Evaluación actualizada.')
            return redirect('pie:detalle', pk=reg.pk)
    else:
        form = EvaluacionPIEForm(instance=ev)
        form.fields['especialista'].queryset = reg.especialistas.all()
    return render(request, 'pie/form_evaluacion.html', {
        'form': form, 'reg': reg, 'ev': ev, 'accion': 'Editar'
    })


# ══════════════════════════════
#  INFORMES DE AVANCE
# ══════════════════════════════

@login_required
def agregar_informe(request, reg_pk):
    reg = get_object_or_404(RegistroPIE, pk=reg_pk)
    if request.method == 'POST':
        form = InformeAvanceForm(request.POST)
        form.fields['especialista'].queryset = reg.especialistas.all()
        if form.is_valid():
            inf = form.save(commit=False)
            inf.registro = reg
            inf.save()
            messages.success(request, '✅ Informe creado.')
            return redirect('pie:informe_pdf', pk=inf.pk)
    else:
        form = InformeAvanceForm(initial={'anno': timezone.now().year})
        form.fields['especialista'].queryset = reg.especialistas.all()
    return render(request, 'pie/form_informe.html', {
        'form': form, 'reg': reg
    })


@login_required
def informe_pdf(request, pk):
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from io import BytesIO

    inf  = get_object_or_404(InformeAvance, pk=pk)
    reg  = inf.registro
    buffer = BytesIO()
    p      = canvas.Canvas(buffer, pagesize=letter)
    ancho, alto = letter

    # Encabezado
    p.setFillColor(colors.HexColor('#0a1628'))
    p.rect(0, alto - 100, ancho, 100, fill=True, stroke=False)
    p.setFillColor(colors.HexColor('#f4c842'))
    p.setFont('Helvetica-Bold', 16)
    p.drawCentredString(ancho / 2, alto - 35, 'LICEO MUNICIPAL — PROGRAMA PIE')
    p.setFont('Helvetica', 11)
    p.drawCentredString(ancho / 2, alto - 55, 'Informe de Avance')
    p.setFillColor(colors.HexColor('#94a3b8'))
    p.setFont('Helvetica', 9)
    p.drawCentredString(ancho / 2, alto - 72,
        f'Año {inf.anno} — {inf.get_trimestre_display()} — Emitido: {inf.fecha_emision.strftime("%d/%m/%Y")}')

    # Datos alumno
    y = alto - 130
    p.setFillColor(colors.HexColor('#1e293b'))
    p.rect(40, y - 55, ancho - 80, 60, fill=True, stroke=False)
    p.setFillColor(colors.HexColor('#f4c842'))
    p.setFont('Helvetica-Bold', 8)
    p.drawString(55, y - 8, 'DATOS DEL ALUMNO')
    p.setFillColor(colors.white)
    p.setFont('Helvetica-Bold', 12)
    p.drawString(55, y - 24, f'{reg.alumno.nombre} {reg.alumno.apellido}')
    p.setFillColor(colors.HexColor('#94a3b8'))
    p.setFont('Helvetica', 9)
    p.drawString(55, y - 38,
        f'Curso: {reg.alumno.curso}   |   Necesidad: {reg.get_necesidad_display()}   |   Nivel: {reg.get_nivel_apoyo_display()}')
    if inf.especialista:
        p.drawString(55, y - 52, f'Especialista: {inf.especialista.nombre} — {inf.especialista.get_especialidad_display()}')

    def bloque(titulo, contenido, y_pos, color_titulo='#f4c842'):
        p.setFillColor(colors.HexColor('#0f172a'))
        p.rect(40, y_pos - 18, ancho - 80, 20, fill=True, stroke=False)
        p.setFillColor(colors.HexColor(color_titulo))
        p.setFont('Helvetica-Bold', 9)
        p.drawString(50, y_pos - 11, titulo.upper())
        lineas   = _wrap_text(contenido, 88)
        altura   = len(lineas) * 14 + 14
        p.setFillColor(colors.HexColor('#1e293b'))
        p.rect(40, y_pos - 18 - altura, ancho - 80, altura, fill=True, stroke=False)
        p.setFillColor(colors.HexColor('#cbd5e1'))
        p.setFont('Helvetica', 9)
        yy = y_pos - 32
        for linea in lineas:
            p.drawString(50, yy, linea)
            yy -= 14
        return y_pos - 18 - altura - 8

    y = alto - 210
    y = bloque('✅ Logros del Período',           inf.logros,          y, '#86efac')
    y = bloque('⚠️ Dificultades Observadas',      inf.dificultades,    y, '#fca5a5')
    y = bloque('💡 Sugerencias y Próximos Pasos', inf.sugerencias,     y, '#fde68a')

    # Mensaje para apoderado en caja especial
    y -= 5
    p.setFillColor(colors.HexColor('#0f2a1a'))
    p.rect(40, y - 20, ancho - 80, 22, fill=True, stroke=False)
    p.setFillColor(colors.HexColor('#86efac'))
    p.setFont('Helvetica-Bold', 9)
    p.drawString(50, y - 13, '💌 MENSAJE PARA EL APODERADO')
    lineas_ap = _wrap_text(inf.para_apoderado, 88)
    altura_ap = len(lineas_ap) * 14 + 14
    p.setFillColor(colors.HexColor('#0d2318'))
    p.rect(40, y - 20 - altura_ap, ancho - 80, altura_ap, fill=True, stroke=False)
    p.setFillColor(colors.HexColor('#bbf7d0'))
    p.setFont('Helvetica', 9)
    yy = y - 34
    for linea in lineas_ap:
        p.drawString(50, yy, linea)
        yy -= 14

    # Firmas
    y = y - 20 - altura_ap - 35
    p.setStrokeColor(colors.HexColor('#334155'))
    p.line(55, y, 240, y)
    p.line(ancho - 240, y, ancho - 55, y)
    p.setFillColor(colors.HexColor('#64748b'))
    p.setFont('Helvetica', 8)
    p.drawCentredString(147, y - 12,
        inf.especialista.nombre if inf.especialista else 'Especialista')
    p.drawCentredString(ancho - 147, y - 12, 'Director/a del establecimiento')

    p.showPage()
    p.save()
    buffer.seek(0)
    nombre = f'Informe_PIE_{reg.alumno.apellido}_{inf.anno}_T{inf.trimestre}.pdf'
    resp   = HttpResponse(buffer, content_type='application/pdf')
    resp['Content-Disposition'] = f'attachment; filename="{nombre}"'
    return resp
