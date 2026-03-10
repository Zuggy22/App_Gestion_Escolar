from django.db import models


class Alumno(models.Model):
    nombre   = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    edad     = models.IntegerField()
    correo   = models.EmailField(unique=True)
    curso    = models.CharField(max_length=10, default='Sin asignar')
    promedio = models.FloatField(default=0.0)

    class Meta:
        verbose_name = 'Alumno'
        verbose_name_plural = 'Alumnos'
        ordering = ['apellido', 'nombre']

    def __str__(self):
        return f'{self.nombre} {self.apellido}'