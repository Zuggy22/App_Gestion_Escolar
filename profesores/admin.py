from django.contrib import admin
from .models import Profesor


@admin.register(Profesor)
class ProfesorAdmin(admin.ModelAdmin):
    list_display  = ['nombre', 'especialidad', 'años_experiencia']
    list_filter   = ['especialidad']
    search_fields = ['nombre', 'especialidad']
    ordering      = ['nombre']