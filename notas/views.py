# notas/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from alumnos.models import Alumno
from cursos.models import Curso          # ← Curso viene de la app cursos
import datetime
from .models import Nota, Asistencia, Observacion, ASIGNATURAS
from .forms  import NotaForm, AsistenciaForm, AsistenciaMasivaForm, ObservacionForm
from django.http import HttpResponse
from django.template.loader import render_to_string
import io


# ─────────────────────────────────────────
# NOTAS
# ─────────────────────────────────────────

@login_required
def notas_alumno(request, alumno_pk):
    alumno = get_object_or_404(Alumno, pk=alumno_pk)
    notas  = Nota.objects.filter(alumno=alumno)

    promedios = [n.promedio_asignatura() for n in notas if n.promedio_asignatura() is not None]
    promedio_final = round(sum(promedios) / len(promedios), 1) if promedios else None

    if promedio_final:
        alumno.promedio = promedio_final
        alumno.save()

    return render(request, 'notas/notas_alumno.html', {
        'alumno':         alumno,
        'notas':          notas,
        'promedio_final': promedio_final,
    })
@login_required
def agregar_nota(request, alumno_pk):
    alumno = get_object_or_404(Alumno, pk=alumno_pk)

    if request.method == 'POST':
        formulario = NotaForm(request.POST)
        if formulario.is_valid():
            asignatura    = formulario.cleaned_data['asignatura']
            nota_existente = Nota.objects.filter(
                alumno=alumno,
                asignatura=asignatura
            ).first()

            if nota_existente:
                formulario = NotaForm(request.POST, instance=nota_existente)
                formulario.save()
                messages.success(request, f'✅ Notas de {asignatura} actualizadas.')
            else:
                nota        = formulario.save(commit=False)
                nota.alumno = alumno
                nota.save()
                messages.success(request, f'✅ Notas de {asignatura} registradas.')

            return redirect('notas:notas_alumno', alumno_pk=alumno.pk)
    else:
        formulario = NotaForm()

    return render(request, 'notas/agregar_nota.html', {
        'formulario': formulario,
        'alumno':     alumno,
    })
@login_required
def eliminar_nota(request, nota_pk):
    nota      = get_object_or_404(Nota, pk=nota_pk)
    alumno_pk = nota.alumno.pk
    if request.method == 'POST':
        asignatura = nota.asignatura
        nota.delete()
        messages.error(request, f'🗑️ Notas de {asignatura} eliminadas.')
        return redirect('notas:notas_alumno', alumno_pk=alumno_pk)
    return render(request, 'notas/confirmar_eliminar_nota.html', {'nota': nota})
@login_required
def promedio_curso(request, curso_nombre):
    alumnos = Alumno.objects.filter(curso=curso_nombre)

    datos_alumnos    = []
    promedios_validos = []

    for alumno in alumnos:
        notas     = Nota.objects.filter(alumno=alumno)
        promedios = [n.promedio_asignatura() for n in notas if n.promedio_asignatura()]
        prom      = round(sum(promedios) / len(promedios), 1) if promedios else None
        if prom:
            promedios_validos.append(prom)
        datos_alumnos.append({'alumno': alumno, 'promedio': prom})

    promedio_general = round(
        sum(promedios_validos) / len(promedios_validos), 1
    ) if promedios_validos else None

    return render(request, 'notas/promedio_curso.html', {
        'curso':            curso_nombre,
        'datos_alumnos':    datos_alumnos,
        'promedio_general': promedio_general,
        'total_alumnos':    alumnos.count(),
    })
@login_required
def resumen_cursos(request):
    cursos = Alumno.objects.values_list('curso', flat=True).distinct()

    datos_cursos = []
    for curso_nombre in cursos:
        if not curso_nombre:
            continue
        alumnos   = Alumno.objects.filter(curso=curso_nombre)
        promedios = []
        for alumno in alumnos:
            notas      = Nota.objects.filter(alumno=alumno)
            prom_notas = [n.promedio_asignatura() for n in notas if n.promedio_asignatura()]
            if prom_notas:
                promedios.append(round(sum(prom_notas) / len(prom_notas), 1))

        promedio_c = round(sum(promedios) / len(promedios), 1) if promedios else None
        datos_cursos.append({
            'curso':    curso_nombre,
            'promedio': promedio_c,
            'alumnos':  alumnos.count(),
        })

    datos_cursos.sort(key=lambda x: x['promedio'] or 0, reverse=True)

    return render(request, 'notas/resumen_cursos.html', {
        'datos_cursos': datos_cursos,
    })


# ─────────────────────────────────────────
# ASISTENCIA
# ─────────────────────────────────────────

@login_required
def registrar_asistencia(request, alumno_pk):
    alumno = get_object_or_404(Alumno, pk=alumno_pk)

    if request.method == 'POST':
        formulario = AsistenciaForm(request.POST)
        if formulario.is_valid():
            asignatura = formulario.cleaned_data['asignatura']
            fecha      = formulario.cleaned_data['fecha']
            estado     = formulario.cleaned_data['estado']

            asistencia, creada = Asistencia.objects.update_or_create(
                alumno=alumno,
                asignatura=asignatura,
                fecha=fecha,
                defaults={'estado': estado}
            )

            if creada:
                messages.success(request, f'✅ Asistencia del {fecha} en {asignatura} registrada.')
            else:
                messages.success(request, f'✅ Asistencia del {fecha} en {asignatura} actualizada.')

            return redirect('notas:asistencia_alumno', alumno_pk=alumno.pk)
    else:
        formulario = AsistenciaForm(initial={'fecha': datetime.date.today()})

    return render(request, 'notas/registrar_asistencia.html', {
        'formulario': formulario,
        'alumno':     alumno,
    })
@login_required
def asistencia_alumno(request, alumno_pk):
    alumno     = get_object_or_404(Alumno, pk=alumno_pk)
    asignaturas = [a[0] for a in ASIGNATURAS]

    resumen = []
    for asignatura in asignaturas:
        datos_asist   = Asistencia.porcentaje_asistencia(alumno, asignatura)
        nota_obj      = Nota.objects.filter(alumno=alumno, asignatura=asignatura).first()
        promedio_nota = nota_obj.promedio_asignatura() if nota_obj else None
        aprobacion    = Asistencia.estado_aprobacion(datos_asist['porcentaje'], promedio_nota)
        historial     = Asistencia.objects.filter(
            alumno=alumno, asignatura=asignatura
        ).order_by('-fecha')[:10]

        resumen.append({
            'asignatura':    asignatura,
            'porcentaje':    datos_asist['porcentaje'],
            'presentes':     datos_asist['presentes'],
            'total_clases':  datos_asist['total'],
            'promedio_nota': promedio_nota,
            'aprobacion':    aprobacion,
            'historial':     historial,
        })

    resumen_con_datos = [r for r in resumen if r['total_clases'] > 0 or r['promedio_nota']]

    return render(request, 'notas/asistencia_alumno.html', {
        'alumno':  alumno,
        'resumen': resumen_con_datos,
        'todas':   resumen,
    })
@login_required
def asistencia_curso(request, curso_nombre):
    alumnos = Alumno.objects.filter(curso=curso_nombre)

    if request.method == 'POST':
        asignatura = request.POST.get('asignatura')
        fecha_str  = request.POST.get('fecha')
        fecha      = datetime.date.fromisoformat(fecha_str)

        for alumno in alumnos:
            estado = request.POST.get(f'estado_{alumno.pk}', 'Ausente')
            Asistencia.objects.update_or_create(
                alumno=alumno,
                asignatura=asignatura,
                fecha=fecha,
                defaults={'estado': estado}
            )

        messages.success(
            request,
            f'✅ Asistencia del {fecha} en {asignatura} registrada para {alumnos.count()} alumnos.'
        )
        return redirect('notas:resumen_asistencia_curso', curso_nombre=curso_nombre)

    formulario = AsistenciaMasivaForm(initial={'fecha': datetime.date.today()})

    return render(request, 'notas/asistencia_curso.html', {
        'formulario':  formulario,
        'alumnos':     alumnos,
        'curso':       curso_nombre,
        'asignaturas': ASIGNATURAS,
        'hoy':         datetime.date.today().strftime('%Y-%m-%d'),
    })
@login_required
def resumen_asistencia_curso(request, curso_nombre):
    alumnos     = Alumno.objects.filter(curso=curso_nombre)
    asignaturas = [a[0] for a in ASIGNATURAS]

    datos = []
    for alumno in alumnos:
        materias               = []
        aprobadas = reprobadas = sin_datos = 0

        for asignatura in asignaturas:
            asist      = Asistencia.porcentaje_asistencia(alumno, asignatura)
            nota_obj   = Nota.objects.filter(alumno=alumno, asignatura=asignatura).first()
            promedio   = nota_obj.promedio_asignatura() if nota_obj else None
            aprobacion = Asistencia.estado_aprobacion(asist['porcentaje'], promedio)

            if aprobacion['estado'] == 'Aprobado':
                aprobadas += 1
            elif aprobacion['estado'] == 'Reprobado':
                reprobadas += 1
            else:
                sin_datos += 1

            materias.append({
                'asignatura': asignatura,
                'porcentaje': asist['porcentaje'],
                'promedio':   promedio,
                'aprobacion': aprobacion,
            })

        datos.append({
            'alumno':     alumno,
            'materias':   materias,
            'aprobadas':  aprobadas,
            'reprobadas': reprobadas,
            'sin_datos':  sin_datos,
        })

    return render(request, 'notas/resumen_asistencia_curso.html', {
        'datos':       datos,
        'curso':       curso_nombre,
        'asignaturas': asignaturas,
    })
@login_required
def resumen_asistencia_general(request):
    """Muestra todos los cursos disponibles para ver asistencia."""
    cursos = Alumno.objects.values_list('curso', flat=True).distinct()
    cursos = [c for c in cursos if c]
    return render(request, 'notas/resumen_asistencia_general.html', {
        'cursos': cursos,
    })

@login_required
def informe_alumno(request, alumno_pk):
    """Informe completo del alumno: notas, asistencia, observaciones."""
    alumno      = get_object_or_404(Alumno, pk=alumno_pk)
    asignaturas = [a[0] for a in ASIGNATURAS]
    notas       = Nota.objects.filter(alumno=alumno)
    observaciones = Observacion.objects.filter(alumno=alumno)

    # Construir resumen completo por asignatura
    resumen = []
    for asignatura in asignaturas:
        nota_obj    = notas.filter(asignatura=asignatura).first()
        asist       = Asistencia.porcentaje_asistencia(alumno, asignatura)
        promedio    = nota_obj.promedio_asignatura() if nota_obj else None
        aprobacion  = Asistencia.estado_aprobacion(asist['porcentaje'], promedio)
        resumen.append({
            'asignatura':   asignatura,
            'nota_1':       nota_obj.nota_1 if nota_obj else None,
            'nota_2':       nota_obj.nota_2 if nota_obj else None,
            'nota_3':       nota_obj.nota_3 if nota_obj else None,
            'nota_4':       nota_obj.nota_4 if nota_obj else None,
            'promedio':     promedio,
            'porcentaje':   asist['porcentaje'],
            'presentes':    asist['presentes'],
            'total_clases': asist['total'],
            'aprobacion':   aprobacion,
        })

    # Promedio final
    promedios_validos = [r['promedio'] for r in resumen if r['promedio']]
    promedio_final = round(
        sum(promedios_validos) / len(promedios_validos), 1
    ) if promedios_validos else None

    # Conteos
    aprobadas  = sum(1 for r in resumen if r['aprobacion']['estado'] == 'Aprobado')
    reprobadas = sum(1 for r in resumen if r['aprobacion']['estado'] == 'Reprobado')

    # Formulario de observación
    if request.method == 'POST':
        form = ObservacionForm(request.POST)
        if form.is_valid():
            obs          = form.save(commit=False)
            obs.alumno   = alumno
            obs.usuario  = request.user
            obs.save()
            messages.success(request, '✅ Observación registrada correctamente.')
            return redirect('notas:informe_alumno', alumno_pk=alumno.pk)
    else:
        form = ObservacionForm()

    return render(request, 'notas/informe_alumno.html', {
        'alumno':        alumno,
        'resumen':       resumen,
        'promedio_final': promedio_final,
        'aprobadas':     aprobadas,
        'reprobadas':    reprobadas,
        'observaciones': observaciones,
        'form':          form,
        'fecha_hoy':     datetime.date.today(),
    })
@login_required
def eliminar_observacion(request, obs_pk):
    obs = get_object_or_404(Observacion, pk=obs_pk)
    alumno_pk = obs.alumno.pk
    if request.method == 'POST':
        obs.delete()
        messages.success(request, '🗑️ Observación eliminada.')
    return redirect('notas:informe_alumno', alumno_pk=alumno_pk)

@login_required
def informe_pdf(request, alumno_pk):
    """Genera el informe del alumno en PDF usando ReportLab."""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
    from reportlab.lib.enums import TA_CENTER, TA_LEFT

    alumno      = get_object_or_404(Alumno, pk=alumno_pk)
    asignaturas = [a[0] for a in ASIGNATURAS]
    notas_qs    = Nota.objects.filter(alumno=alumno)
    observaciones = Observacion.objects.filter(alumno=alumno)

    # Construir datos
    resumen = []
    for asignatura in asignaturas:
        nota_obj   = notas_qs.filter(asignatura=asignatura).first()
        asist      = Asistencia.porcentaje_asistencia(alumno, asignatura)
        promedio   = nota_obj.promedio_asignatura() if nota_obj else None
        aprobacion = Asistencia.estado_aprobacion(asist['porcentaje'], promedio)
        resumen.append({
            'asignatura': asignatura,
            'n1': str(nota_obj.nota_1) if nota_obj and nota_obj.nota_1 else '—',
            'n2': str(nota_obj.nota_2) if nota_obj and nota_obj.nota_2 else '—',
            'n3': str(nota_obj.nota_3) if nota_obj and nota_obj.nota_3 else '—',
            'n4': str(nota_obj.nota_4) if nota_obj and nota_obj.nota_4 else '—',
            'promedio':   str(promedio) if promedio else '—',
            'asistencia': f"{asist['porcentaje']}%" if asist['porcentaje'] else '—',
            'estado':     aprobacion['estado'],
        })

    promedios_v = [r for r in resumen if r['promedio'] != '—']
    promedio_final = round(
        sum(float(r['promedio']) for r in promedios_v) / len(promedios_v), 1
    ) if promedios_v else None

    # Crear PDF
    buffer   = io.BytesIO()
    doc      = SimpleDocTemplate(
        buffer, pagesize=A4,
        topMargin=2*cm, bottomMargin=2*cm,
        leftMargin=2*cm, rightMargin=2*cm
    )
    story    = []
    styles   = getSampleStyleSheet()

    # Colores corporativos
    NAVY   = colors.HexColor('#0a1628')
    GOLD   = colors.HexColor('#f4c842')
    WHITE  = colors.white
    GREEN  = colors.HexColor('#22c55e')
    RED    = colors.HexColor('#ef4444')
    GRAY   = colors.HexColor('#94a3b8')
    DARK   = colors.HexColor('#1e3f7a')

    # Estilos
    title_style = ParagraphStyle(
        'Title', parent=styles['Normal'],
        fontSize=20, textColor=NAVY,
        fontName='Helvetica-Bold',
        alignment=TA_CENTER, spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'Subtitle', parent=styles['Normal'],
        fontSize=11, textColor=GRAY,
        alignment=TA_CENTER, spaceAfter=2
    )
    section_style = ParagraphStyle(
        'Section', parent=styles['Normal'],
        fontSize=10, textColor=NAVY,
        fontName='Helvetica-Bold',
        spaceBefore=12, spaceAfter=6
    )
    body_style = ParagraphStyle(
        'Body', parent=styles['Normal'],
        fontSize=9, textColor=colors.HexColor('#374151'),
        spaceAfter=3
    )

    # ── ENCABEZADO ──
    story.append(Paragraph('LICEO MUNICIPAL', title_style))
    story.append(Paragraph('Sistema de Gestión Escolar', subtitle_style))
    story.append(Spacer(1, 0.3*cm))
    story.append(HRFlowable(width='100%', thickness=2, color=GOLD))
    story.append(Spacer(1, 0.4*cm))
    story.append(Paragraph('INFORME ACADÉMICO DEL ALUMNO', ParagraphStyle(
        'InfoTitle', parent=styles['Normal'],
        fontSize=14, textColor=DARK,
        fontName='Helvetica-Bold', alignment=TA_CENTER
    )))
    story.append(Spacer(1, 0.5*cm))

    # ── DATOS PERSONALES ──
    story.append(Paragraph('▌ DATOS DEL ALUMNO', section_style))
    datos_tabla = [
        ['Nombre completo:', f'{alumno.nombre} {alumno.apellido}',
         'Curso:', alumno.curso or '—'],
        ['RUT:', alumno.rut or 'Sin RUT',
         'Edad:', f'{alumno.edad} años' if alumno.edad else '—'],
        ['Correo:', alumno.correo or '—',
         'Promedio final:', str(promedio_final) if promedio_final else 'Sin datos'],
        ['Fecha de informe:', datetime.date.today().strftime('%d/%m/%Y'),
         '', ''],
    ]
    tabla_datos = Table(datos_tabla, colWidths=[3.5*cm, 6*cm, 2.5*cm, 5*cm])
    tabla_datos.setStyle(TableStyle([
        ('FONTNAME',    (0,0), (-1,-1), 'Helvetica'),
        ('FONTNAME',    (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME',    (2,0), (2,-1), 'Helvetica-Bold'),
        ('FONTSIZE',    (0,0), (-1,-1), 9),
        ('TEXTCOLOR',   (0,0), (0,-1), NAVY),
        ('TEXTCOLOR',   (2,0), (2,-1), NAVY),
        ('TEXTCOLOR',   (1,0), (1,-1), colors.HexColor('#374151')),
        ('TEXTCOLOR',   (3,0), (3,-1), colors.HexColor('#374151')),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.HexColor('#f8fafc'), WHITE]),
        ('GRID',        (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING',     (0,0), (-1,-1), 6),
        ('VALIGN',      (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(tabla_datos)
    story.append(Spacer(1, 0.5*cm))

    # ── TABLA DE NOTAS Y ASISTENCIA ──
    story.append(Paragraph('▌ RENDIMIENTO POR ASIGNATURA', section_style))

    headers = ['Asignatura', 'N1', 'N2', 'N3', 'N4', 'Promedio', 'Asistencia', 'Estado']
    tabla_data = [headers]
    for r in resumen:
        tabla_data.append([
            r['asignatura'], r['n1'], r['n2'], r['n3'], r['n4'],
            r['promedio'], r['asistencia'], r['estado']
        ])

    tabla_notas = Table(
        tabla_data,
        colWidths=[4*cm, 1.2*cm, 1.2*cm, 1.2*cm, 1.2*cm, 2*cm, 2.2*cm, 2.2*cm]
    )
    estilo_notas = [
        # Header
        ('BACKGROUND',  (0,0), (-1,0), NAVY),
        ('TEXTCOLOR',   (0,0), (-1,0), WHITE),
        ('FONTNAME',    (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',    (0,0), (-1,-1), 8),
        ('ALIGN',       (0,0), (-1,-1), 'CENTER'),
        ('ALIGN',       (0,0), (0,-1), 'LEFT'),
        ('VALIGN',      (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING',     (0,0), (-1,-1), 5),
        ('GRID',        (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#f8fafc'), WHITE]),
    ]
    # Colorear estado
    for i, r in enumerate(resumen, start=1):
        if r['estado'] == 'Aprobado':
            estilo_notas.append(('TEXTCOLOR', (7,i), (7,i), GREEN))
            estilo_notas.append(('FONTNAME',  (7,i), (7,i), 'Helvetica-Bold'))
        elif r['estado'] == 'Reprobado':
            estilo_notas.append(('TEXTCOLOR', (7,i), (7,i), RED))
            estilo_notas.append(('FONTNAME',  (7,i), (7,i), 'Helvetica-Bold'))
        # Colorear promedio
        if r['promedio'] != '—':
            prom = float(r['promedio'])
            col  = GREEN if prom >= 5.5 else RED
            estilo_notas.append(('TEXTCOLOR', (5,i), (5,i), col))
            estilo_notas.append(('FONTNAME',  (5,i), (5,i), 'Helvetica-Bold'))

    tabla_notas.setStyle(TableStyle(estilo_notas))
    story.append(tabla_notas)
    story.append(Spacer(1, 0.3*cm))

    # ── RESUMEN FINAL ──
    aprobadas  = sum(1 for r in resumen if r['estado'] == 'Aprobado')
    reprobadas = sum(1 for r in resumen if r['estado'] == 'Reprobado')

    resumen_data = [[
        'Promedio Final',
        str(promedio_final) if promedio_final else '—',
        'Asignaturas Aprobadas',
        str(aprobadas),
        'Asignaturas Reprobadas',
        str(reprobadas),
    ]]
    tabla_resumen = Table(resumen_data, colWidths=[3.5*cm, 2.5*cm, 4*cm, 1.5*cm, 4*cm, 1.5*cm])
    tabla_resumen.setStyle(TableStyle([
        ('BACKGROUND',  (0,0), (-1,-1), NAVY),
        ('TEXTCOLOR',   (0,0), (-1,-1), WHITE),
        ('FONTNAME',    (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTNAME',    (1,0), (1,0), 'Helvetica-Bold'),
        ('TEXTCOLOR',   (1,0), (1,0), GOLD),
        ('TEXTCOLOR',   (3,0), (3,0), GREEN),
        ('TEXTCOLOR',   (5,0), (5,0), RED),
        ('FONTSIZE',    (0,0), (-1,-1), 9),
        ('ALIGN',       (0,0), (-1,-1), 'CENTER'),
        ('VALIGN',      (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING',     (0,0), (-1,-1), 8),
        ('GRID',        (0,0), (-1,-1), 0.5, DARK),
    ]))
    story.append(tabla_resumen)
    story.append(Spacer(1, 0.5*cm))

    # ── OBSERVACIONES ──
    story.append(Paragraph('▌ OBSERVACIONES', section_style))
    if observaciones.exists():
        for obs in observaciones:
            cat_colors = {
                'academica':  '#6366f1',
                'conductual': '#ef4444',
                'familiar':   '#f4c842',
                'medica':     '#14b8a6',
            }
            color_hex = cat_colors.get(obs.categoria, '#6366f1')
            obs_data = [[
                Paragraph(f'<b>{obs.get_categoria_display()}</b>', ParagraphStyle(
                    'Cat', parent=styles['Normal'],
                    fontSize=8, textColor=colors.HexColor(color_hex),
                    fontName='Helvetica-Bold'
                )),
                Paragraph(obs.texto, body_style),
                Paragraph(
                    f'{obs.fecha.strftime("%d/%m/%Y %H:%M")}<br/>{obs.usuario.username if obs.usuario else "—"}',
                    ParagraphStyle('Date', parent=styles['Normal'], fontSize=7, textColor=GRAY)
                ),
            ]]
            tabla_obs = Table(obs_data, colWidths=[2.5*cm, 11*cm, 3.5*cm])
            tabla_obs.setStyle(TableStyle([
                ('FONTSIZE',  (0,0), (-1,-1), 8),
                ('VALIGN',    (0,0), (-1,-1), 'TOP'),
                ('PADDING',   (0,0), (-1,-1), 6),
                ('GRID',      (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
                ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.HexColor('#f8fafc')]),
            ]))
            story.append(tabla_obs)
            story.append(Spacer(1, 0.15*cm))
    else:
        story.append(Paragraph('Sin observaciones registradas.', body_style))

    story.append(Spacer(1, 0.5*cm))

    # ── FIRMA ──
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#e2e8f0')))
    story.append(Spacer(1, 0.3*cm))
    firma_data = [[
        Paragraph('_______________________\nProfesor / Encargado', ParagraphStyle(
            'Firma', parent=styles['Normal'], fontSize=8,
            textColor=GRAY, alignment=TA_CENTER
        )),
        Paragraph(
            f'Generado el {datetime.date.today().strftime("%d/%m/%Y")}<br/>Liceo Municipal · Sistema de Gestión',
            ParagraphStyle('Footer', parent=styles['Normal'], fontSize=7,
                           textColor=GRAY, alignment=TA_CENTER)
        ),
        Paragraph('_______________________\nDirector(a)', ParagraphStyle(
            'Firma2', parent=styles['Normal'], fontSize=8,
            textColor=GRAY, alignment=TA_CENTER
        )),
    ]]
    tabla_firma = Table(firma_data, colWidths=[5.5*cm, 6*cm, 5.5*cm])
    tabla_firma.setStyle(TableStyle([
        ('ALIGN',   (0,0), (-1,-1), 'CENTER'),
        ('VALIGN',  (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(tabla_firma)

    # Construir PDF
    doc.build(story)
    buffer.seek(0)
    nombre_archivo = f'informe_{alumno.apellido}_{alumno.nombre}.pdf'
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
    return response

# ── Libro de clases por profesor ───────────────────────────
def libro_clases(request):
    from profesores.models import Profesor
    from .models import Nota

    profesores  = Profesor.objects.all().order_by('nombre')
    prof_id     = request.GET.get('profesor', '')
    curso_sel   = request.GET.get('curso', '')
    asignatura  = request.GET.get('asignatura', '')

    profesor_obj  = None
    cursos_profe  = []
    tabla         = []
    asignaturas   = [a[0] for a in ASIGNATURAS]

    if prof_id:
        try:
            profesor_obj = Profesor.objects.get(pk=prof_id)
            # Cursos donde este profesor es jefe
            from cursos.models import Curso
            cursos_profe = Curso.objects.filter(
                profesor_jefe=profesor_obj
            ).values_list('nombre_ramo', flat=True).distinct()

            if curso_sel:
                alumnos = Alumno.objects.filter(
                    curso=curso_sel
                ).order_by('apellido')

                for alumno in alumnos:
                    fila = {'alumno': alumno, 'asignaturas': []}
                    notas_alumno = Nota.objects.filter(alumno=alumno)
                    promedio_final_sum = []

                    for asig in asignaturas:
                        nota_obj = notas_alumno.filter(asignatura=asig).first()
                        if nota_obj:
                            prom = nota_obj.promedio_asignatura()
                            if prom:
                                promedio_final_sum.append(float(prom))
                            fila['asignaturas'].append({
                                'nombre':  asig,
                                'nota_1':  nota_obj.nota_1,
                                'nota_2':  nota_obj.nota_2,
                                'nota_3':  nota_obj.nota_3,
                                'nota_4':  nota_obj.nota_4,
                                'promedio': prom,
                                'estado':  nota_obj.estado(),
                            })
                        else:
                            fila['asignaturas'].append({
                                'nombre':  asig,
                                'nota_1':  None,
                                'nota_2':  None,
                                'nota_3':  None,
                                'nota_4':  None,
                                'promedio': None,
                                'estado':  'Sin notas',
                            })

                    fila['promedio_final'] = round(
                        sum(promedio_final_sum) / len(promedio_final_sum), 1
                    ) if promedio_final_sum else None
                    tabla.append(fila)

        except Profesor.DoesNotExist:
            pass

    return render(request, 'notas/libro_clases.html', {
        'profesores':   profesores,
        'prof_id':      prof_id,
        'profesor_obj': profesor_obj,
        'cursos_profe': cursos_profe,
        'curso_sel':    curso_sel,
        'tabla':        tabla,
        'asignaturas':  asignaturas,
    })