from django.contrib import admin
from .models import Apoderado, MensajeApoderado

@admin.register(Apoderado)
class ApoderadoAdmin(admin.ModelAdmin):
    list_display  = ['nombre', 'rut', 'relacion', 'alumno', 'telefono', 'correo']
    list_filter   = ['relacion']
    search_fields = ['nombre', 'rut', 'alumno__nombre']

@admin.register(MensajeApoderado)
class MensajeAdmin(admin.ModelAdmin):
    list_display  = ['apoderado', 'asunto', 'categoria', 'estado', 'fecha_envio']
    list_filter   = ['estado', 'categoria']
    search_fields = ['apoderado__nombre', 'asunto']