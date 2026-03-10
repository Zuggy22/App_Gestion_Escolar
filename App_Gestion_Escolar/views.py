from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from alumnos.models import Alumno
from profesores.models import Profesor
from cursos.models import Curso
from apoderados.models import Apoderado
from pie.models import RegistroPIE


@login_required
def inicio(request):
    total_alumnos   = Alumno.objects.count()
    total_profesores = Profesor.objects.count()
    total_cursos    = Curso.objects.count()
    total_apoderados = Apoderado.objects.count()
    total_pie       = RegistroPIE.objects.filter(activo=True).count()
    alumnos_riesgo  = Alumno.objects.filter(promedio__lt=5.5).count()

    return render(request, 'inicio.html', {
        'total_alumnos':    total_alumnos,
        'total_profesores': total_profesores,
        'total_cursos':     total_cursos,
        'total_apoderados': total_apoderados,
        'total_pie':        total_pie,
        'alumnos_riesgo':   alumnos_riesgo,
    })
