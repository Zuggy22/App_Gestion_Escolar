from django.db import models


class Profesor(models.Model):
    nombre           = models.CharField(max_length=100)
    especialidad     = models.CharField(max_length=100)
    años_experiencia = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Profesor'
        verbose_name_plural = 'Profesores'
        ordering = ['nombre']

    def __str__(self):
        return f'Prof. {self.nombre} — {self.especialidad}'
