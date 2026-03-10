from django.db import models
from alumnos.models import Alumno

ASIGNATURAS = [
    ('Lenguaje',          'Lenguaje'),
    ('Matemáticas',       'Matemáticas'),
    ('Ciencias',          'Ciencias'),
    ('Historia',          'Historia'),
    ('Inglés',            'Inglés'),
    ('Educación Física',  'Educación Física'),
    ('Artes',             'Artes'),
]


class Nota(models.Model):
    alumno      = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='notas')
    asignatura  = models.CharField(max_length=50, choices=ASIGNATURAS)
    nota_1      = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    nota_2      = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    nota_3      = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    nota_4      = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)

    class Meta:
        unique_together = ['alumno', 'asignatura']
        verbose_name        = 'Nota'
        verbose_name_plural = 'Notas'

    def __str__(self):
        return f'{self.alumno} — {self.asignatura}'

    def promedio_asignatura(self):
        notas = [n for n in [self.nota_1, self.nota_2, self.nota_3, self.nota_4] if n is not None]
        if not notas:
            return None
        return round(sum(float(n) for n in notas) / len(notas), 1)

    def estado(self):
        promedio = self.promedio_asignatura()
        if promedio is None:
            return 'Sin notas'
        return 'Aprobado' if promedio >= 5.5 else 'Reprobado'


class Asistencia(models.Model):
    ESTADOS = [
        ('Presente', 'Presente'),
        ('Ausente',  'Ausente'),
    ]

    alumno     = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='asistencias')
    asignatura = models.CharField(max_length=50, choices=ASIGNATURAS)
    fecha      = models.DateField()
    estado     = models.CharField(max_length=10, choices=ESTADOS, default='Presente')

    class Meta:
        unique_together     = ['alumno', 'asignatura', 'fecha']
        verbose_name        = 'Asistencia'
        verbose_name_plural = 'Asistencias'

    def __str__(self):
        return f'{self.alumno} — {self.asignatura} — {self.fecha}'

    @staticmethod
    def porcentaje_asistencia(alumno, asignatura):
        registros = Asistencia.objects.filter(alumno=alumno, asignatura=asignatura)
        total     = registros.count()
        if total == 0:
            return {'porcentaje': None, 'presentes': 0, 'total': 0}
        presentes  = registros.filter(estado='Presente').count()
        porcentaje = round((presentes / total) * 100, 1)
        return {'porcentaje': porcentaje, 'presentes': presentes, 'total': total}

    @staticmethod
    def estado_aprobacion(porcentaje_asist, promedio_nota):
        if porcentaje_asist is None or promedio_nota is None:
            return {
                'estado':  'Sin datos',
                'color':   'gray',
                'emoji':   '⏳',
                'detalle': 'Faltan datos de asistencia o notas.',
            }
        p = float(promedio_nota)
        a = float(porcentaje_asist)
        if a >= 80 and p >= 4.5:
            return {'estado': 'Aprobado', 'color': 'green', 'emoji': '✅',
                    'detalle': f'Asistencia {a}% ≥ 80% y nota {p} ≥ 4.5'}
        elif 70 <= a < 80 and p >= 5.0:
            return {'estado': 'Aprobado', 'color': 'green', 'emoji': '✅',
                    'detalle': f'Asistencia {a}% entre 70%-80% y nota {p} ≥ 5.0'}
        else:
            motivo = []
            if a < 70:
                motivo.append(f'Asistencia {a}% < 70%')
            if p < 4.5:
                motivo.append(f'Nota {p} < 4.5')
            return {'estado': 'Reprobado', 'color': 'red', 'emoji': '❌',
                    'detalle': ' · '.join(motivo)}


# ── NUEVO MODELO ──────────────────────────────────────────
class Observacion(models.Model):
    CATEGORIAS = [
        ('academica',  '📚 Académica'),
        ('conductual', '⚠️ Conductual'),
        ('familiar',   '🏠 Familiar'),
        ('medica',     '🏥 Médica'),
    ]

    alumno    = models.ForeignKey(
        Alumno, on_delete=models.CASCADE, related_name='observaciones'
    )
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, default='academica')
    texto     = models.TextField()
    fecha     = models.DateTimeField(auto_now_add=True)
    usuario   = models.ForeignKey(
        'auth.User', on_delete=models.SET_NULL,
        null=True, related_name='observaciones'
    )

    class Meta:
        verbose_name        = 'Observación'
        verbose_name_plural = 'Observaciones'
        ordering            = ['-fecha']

    def __str__(self):
        return f'{self.alumno} — {self.get_categoria_display()} — {self.fecha:%d/%m/%Y}'

    def color(self):
        colores = {
            'academica':  {'bg': 'rgba(99,102,241,0.15)',  'border': 'rgba(99,102,241,0.3)',  'text': '#a5b4fc'},
            'conductual': {'bg': 'rgba(239,68,68,0.15)',   'border': 'rgba(239,68,68,0.3)',   'text': '#fca5a5'},
            'familiar':   {'bg': 'rgba(244,200,66,0.15)',  'border': 'rgba(244,200,66,0.3)',  'text': '#fde68a'},
            'medica':     {'bg': 'rgba(20,184,166,0.15)',  'border': 'rgba(20,184,166,0.3)',  'text': '#5eead4'},
        }
        return colores.get(self.categoria, colores['academica'])