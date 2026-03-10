from django.urls import path
from . import views

app_name = 'alumnos'

urlpatterns = [
    path('',                   views.lista_alumnos,   name='lista'),
    path('crear/',             views.crear_alumno,    name='crear'),
    path('editar/<int:pk>/',   views.editar_alumno,   name='editar'),
    path('eliminar/<int:pk>/', views.eliminar_alumno, name='eliminar'),
    path('por-curso/', views.alumnos_por_curso, name='por_curso'),
    path('con-apoderados/', views.alumnos_con_apoderados, name='con_apoderados'),
]