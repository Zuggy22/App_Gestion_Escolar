from django.db import models
from alumnos.models import Alumno


class Apoderado(models.Model):
    RELACIONES = [
        ('padre',  '👨 Padre'),
        ('madre',  '👩 Madre'),
        ('tutor',  '🧑 Tutor Legal'),
        ('abuelo', '👴 Abuelo/a'),
        ('otro',   '👤 Otro'),
    ]

    alumno      = models.OneToOneField(
        Alumno, on_delete=models.CASCADE,
        related_name='apoderado'
    )
    nombre      = models.CharField(max_length=100)
    rut         = models.CharField(max_length=12, unique=True)
    relacion    = models.CharField(max_length=20, choices=RELACIONES, default='padre')
    telefono    = models.CharField(max_length=15)
    correo      = models.EmailField()
    direccion   = models.CharField(max_length=200)
    datos_adicionales = models.TextField(blank=True, null=True,
        verbose_name='Datos adicionales')
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = 'Apoderado'
        verbose_name_plural = 'Apoderados'
        ordering            = ['nombre']

    def __str__(self):
        return f'{self.nombre} — Apoderado de {self.alumno}'

    def get_relacion_emoji(self):
        emojis = {
            'padre': '👨', 'madre': '👩',
            'tutor': '🧑', 'abuelo': '👴', 'otro': '👤'
        }
        return emojis.get(self.relacion, '👤')


class MensajeApoderado(models.Model):
    ESTADOS = [
        ('pendiente',   '⏳ Pendiente'),
        ('respondido',  '✅ Respondido'),
        ('cerrado',     '🔒 Cerrado'),
    ]
    CATEGORIAS = [
        ('academico',   '📚 Académico'),
        ('conductual',  '⚠️ Conductual'),
        ('administrativo', '📋 Administrativo'),
        ('salud',       '🏥 Salud'),
        ('otro',        '💬 Otro'),
    ]

    apoderado   = models.ForeignKey(
        Apoderado, on_delete=models.CASCADE,
        related_name='mensajes'
    )
    categoria   = models.CharField(max_length=20, choices=CATEGORIAS, default='academico')
    asunto      = models.CharField(max_length=200)
    mensaje     = models.TextField()
    respuesta   = models.TextField(blank=True, null=True)
    estado      = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    fecha_envio = models.DateTimeField(auto_now_add=True)
    fecha_respuesta = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name        = 'Mensaje de Apoderado'
        verbose_name_plural = 'Mensajes de Apoderados'
        ordering            = ['-fecha_envio']

    def __str__(self):
        return f'{self.apoderado.nombre} — {self.asunto}'

    def color_estado(self):
        colores = {
            'pendiente':  {'bg': 'rgba(234,179,8,0.15)',  'text': '#fde68a', 'border': 'rgba(234,179,8,0.3)'},
            'respondido': {'bg': 'rgba(34,197,94,0.15)',  'text': '#86efac', 'border': 'rgba(34,197,94,0.3)'},
            'cerrado':    {'bg': 'rgba(100,116,139,0.15)','text': '#94a3b8', 'border': 'rgba(100,116,139,0.3)'},
        }
        return colores.get(self.estado, colores['pendiente'])

    def color_categoria(self):
        colores = {
            'academico':      {'text': '#a5b4fc', 'border': 'rgba(99,102,241,0.4)'},
            'conductual':     {'text': '#fca5a5', 'border': 'rgba(239,68,68,0.4)'},
            'administrativo': {'text': '#fde68a', 'border': 'rgba(244,200,66,0.4)'},
            'salud':          {'text': '#5eead4', 'border': 'rgba(20,184,166,0.4)'},
            'otro':           {'text': '#94a3b8', 'border': 'rgba(100,116,139,0.4)'},
        }
        return colores.get(self.categoria, colores['otro'])