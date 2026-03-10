# notas/urls.py
from django.urls import path
from . import views

app_name = 'notas'

urlpatterns = [
    path('alumno/<int:alumno_pk>/',         views.notas_alumno,   name='notas_alumno'),
    path('agregar/<int:alumno_pk>/',        views.agregar_nota,   name='agregar_nota'),
    path('eliminar/<int:nota_pk>/',         views.eliminar_nota,  name='eliminar_nota'),
    path('curso/<str:curso_nombre>/',       views.promedio_curso, name='promedio_curso'),
    path('cursos/',                         views.resumen_cursos, name='resumen_cursos'),
    # Asistencia
    path('asistencia/alumno/<int:alumno_pk>/', views.asistencia_alumno, name='asistencia_alumno'),
    path('asistencia/registrar/<int:alumno_pk>/', views.registrar_asistencia, name='registrar_asistencia'),
    path('asistencia/curso/<str:curso_nombre>/', views.asistencia_curso, name='asistencia_curso'),
    path('asistencia/resumen/<str:curso_nombre>/', views.resumen_asistencia_curso, name='resumen_asistencia_curso'),
    path('asistencia/', views.resumen_asistencia_general, name='resumen_asistencia_general'),
    # Informe y observaciones
    path('informe/<int:alumno_pk>/', views.informe_alumno, name='informe_alumno'),
    path('informe/<int:alumno_pk>/pdf/', views.informe_pdf, name='informe_pdf'),
    path('observacion/eliminar/<int:obs_pk>/', views.eliminar_observacion, name='eliminar_observacion'),
    path('libro-clases/', views.libro_clases, name='libro_clases'),
]