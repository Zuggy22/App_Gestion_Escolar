from django.contrib import admin
from .models import Nota, Asistencia, Observacion


@admin.register(Nota)
class NotaAdmin(admin.ModelAdmin):
    list_display  = ['alumno', 'asignatura', 'nota_1', 'nota_2', 'nota_3', 'nota_4']
    list_filter   = ['asignatura']
    search_fields = ['alumno__nombre', 'alumno__apellido']

@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display  = ['alumno', 'asignatura', 'fecha', 'estado']
    list_filter   = ['asignatura', 'estado', 'fecha']
    search_fields = ['alumno__nombre', 'alumno__apellido']
    date_hierarchy = 'fecha'

@admin.register(Observacion)
class ObservacionAdmin(admin.ModelAdmin):
    list_display  = ['alumno', 'categoria', 'fecha', 'usuario']
    list_filter   = ['categoria', 'fecha']
    search_fields = ['alumno__nombre', 'alumno__apellido', 'texto']