from django.urls import path
from . import views

app_name = 'apoderados'

urlpatterns = [
    path('',                          views.lista_apoderados,  name='lista'),
    path('crear/',                    views.crear_apoderado,   name='crear'),
    path('<int:pk>/',                 views.detalle_apoderado, name='detalle'),
    path('<int:pk>/editar/',          views.editar_apoderado,  name='editar'),
    path('<int:pk>/eliminar/',        views.eliminar_apoderado,name='eliminar'),
    path('<int:apoderado_pk>/mensaje/',views.enviar_mensaje,   name='enviar_mensaje'),
    path('mensaje/<int:msg_pk>/responder/', views.responder_mensaje, name='responder_mensaje'),
    path('bandeja/',                  views.bandeja_mensajes,  name='bandeja'),
]