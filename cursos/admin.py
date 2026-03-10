from django.contrib import admin
from .models import Curso


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display  = ['nombre_ramo', 'nivel', 'jornada', 'profesor_jefe']
    list_filter   = ['nivel', 'jornada']
    search_fields = ['nombre_ramo']
    ordering      = ['nivel']