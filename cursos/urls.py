from django.urls import path
from . import views

app_name = 'cursos'

urlpatterns = [
    path('',                   views.lista_cursos,   name='lista'),
    path('crear/',             views.crear_curso,    name='crear'),
    path('editar/<int:pk>/',   views.editar_curso,   name='editar'),
    path('eliminar/<int:pk>/', views.eliminar_curso, name='eliminar'),
]