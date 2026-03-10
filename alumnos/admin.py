from django.contrib import admin
from .models import Alumno


@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    # Columnas visibles en la lista
    list_display  = ['nombre', 'apellido', 'curso', 'promedio', 'correo']
    # Filtros laterales
    list_filter   = ['curso']
    # Búsqueda por nombre o correo
    search_fields = ['nombre', 'apellido', 'correo']
    # Ordenar por apellido
    ordering      = ['apellido']