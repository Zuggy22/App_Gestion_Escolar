from django.contrib import admin
from .models import Planificacion, MensajeAlumno

@admin.register(Planificacion)
class PlanificacionAdmin(admin.ModelAdmin):
    list_display  = ['tipo', 'unidad_tema', 'profesor', 'curso', 'fecha', 'estado']
    list_filter   = ['tipo', 'estado', 'curso']
    search_fields = ['unidad_tema', 'profesor__nombre']

@admin.register(MensajeAlumno)
class MensajeAlumnoAdmin(admin.ModelAdmin):
    list_display  = ['asunto', 'profesor', 'curso', 'tipo', 'fecha_envio', 'enviado_correo']
    list_filter   = ['tipo', 'enviado_correo']