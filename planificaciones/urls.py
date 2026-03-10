from django.urls import path
from . import views

app_name = 'planificaciones'

urlpatterns = [
    path('',                          views.lista_planificaciones,    name='lista'),
    path('crear/',                    views.crear_planificacion,      name='crear'),
    path('<int:pk>/',                 views.detalle_planificacion,    name='detalle'),
    path('<int:pk>/editar/',          views.editar_planificacion,     name='editar'),
    path('<int:pk>/eliminar/',        views.eliminar_planificacion,   name='eliminar'),
    path('mensajes/',                 views.enviar_mensaje_alumnos,   name='enviar_mensaje'),
    path('mensajes/bandeja/',         views.bandeja_mensajes_alumnos, name='bandeja_mensajes'),
]