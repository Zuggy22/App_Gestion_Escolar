from django.urls import path
from . import views

app_name = 'profesores'

urlpatterns = [
    path('',                   views.lista_profesores,   name='lista'),
    path('crear/',             views.crear_profesor,     name='crear'),
    path('editar/<int:pk>/',   views.editar_profesor,    name='editar'),
    path('eliminar/<int:pk>/', views.eliminar_profesor,  name='eliminar'),
]