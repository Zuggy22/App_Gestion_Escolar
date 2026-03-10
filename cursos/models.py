from django.db import models


class Curso(models.Model):
    JORNADAS = [
        ('Mañana',   'Mañana (08:00 - 14:00)'),
        ('Tarde',    'Tarde (14:00 - 20:00)'),
        ('Completa', 'Jornada Completa'),
    ]
    NIVELES = [
        ('Primero Medio', '1° Medio'),
        ('Segundo Medio', '2° Medio'),
        ('Tercero Medio', '3° Medio'),
        ('Cuarto Medio',  '4° Medio'),
    ]

    nombre_ramo   = models.CharField(max_length=100)
    nivel         = models.CharField(max_length=50, choices=NIVELES)
    jornada       = models.CharField(max_length=50, choices=JORNADAS)
    profesor_jefe = models.ForeignKey(
        'profesores.Profesor',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cursos_a_cargo'
    )

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['nivel', 'nombre_ramo']

    def __str__(self):
        return f'{self.nombre_ramo} — {self.nivel}'
