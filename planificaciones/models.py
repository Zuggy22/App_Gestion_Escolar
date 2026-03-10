from django.db import models
from profesores.models import Profesor
from alumnos.models import Alumno


class Planificacion(models.Model):
    TIPOS = [
        ('clase',   '📘 Clase'),
        ('prueba',  '📝 Prueba'),
        ('trabajo', '📋 Trabajo'),
    ]
    ESTADOS = [
        ('borrador',   '✏️ Borrador'),
        ('publicada',  '✅ Publicada'),
        ('finalizada', '🏁 Finalizada'),
    ]

    profesor        = models.ForeignKey(Profesor, on_delete=models.CASCADE, related_name='planificaciones')
    tipo            = models.CharField(max_length=10, choices=TIPOS, default='clase')
    curso           = models.CharField(max_length=100)
    asignatura      = models.CharField(max_length=100)
    fecha           = models.DateField()
    unidad_tema     = models.CharField(max_length=200)
    objetivos       = models.TextField()
    actividades     = models.TextField()
    recursos        = models.TextField(blank=True)
    estado          = models.CharField(max_length=15, choices=ESTADOS, default='borrador')
    fecha_creacion  = models.DateTimeField(auto_now_add=True)
    fecha_modified  = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = 'Planificación'
        verbose_name_plural = 'Planificaciones'
        ordering            = ['-fecha']

    def __str__(self):
        return f'{self.get_tipo_display()} — {self.curso} — {self.unidad_tema} ({self.fecha})'

    def color_tipo(self):
        colores = {
            'clase':   {'bg': 'rgba(99,102,241,0.12)',  'border': 'rgba(99,102,241,0.3)',  'text': '#a5b4fc'},
            'prueba':  {'bg': 'rgba(239,68,68,0.12)',   'border': 'rgba(239,68,68,0.3)',   'text': '#fca5a5'},
            'trabajo': {'bg': 'rgba(244,200,66,0.12)',  'border': 'rgba(244,200,66,0.3)',  'text': '#fde68a'},
        }
        return colores.get(self.tipo, colores['clase'])

    def color_estado(self):
        colores = {
            'borrador':   {'bg': 'rgba(100,116,139,0.12)', 'border': 'rgba(100,116,139,0.3)', 'text': '#94a3b8'},
            'publicada':  {'bg': 'rgba(34,197,94,0.12)',   'border': 'rgba(34,197,94,0.3)',   'text': '#86efac'},
            'finalizada': {'bg': 'rgba(20,184,166,0.12)',  'border': 'rgba(20,184,166,0.3)',  'text': '#5eead4'},
        }
        return colores.get(self.estado, colores['borrador'])


class MensajeAlumno(models.Model):
    TIPOS = [
        ('aviso',    '📢 Aviso'),
        ('prueba',   '📝 Recordatorio de Prueba'),
        ('trabajo',  '📋 Recordatorio de Trabajo'),
        ('reunion',  '👥 Reunión'),
        ('otro',     '💬 Otro'),
    ]

    profesor        = models.ForeignKey(Profesor, on_delete=models.CASCADE, related_name='mensajes_alumnos')
    planificacion   = models.ForeignKey(Planificacion, on_delete=models.SET_NULL, null=True, blank=True, related_name='mensajes')
    tipo            = models.CharField(max_length=15, choices=TIPOS, default='aviso')
    curso           = models.CharField(max_length=100)
    asunto          = models.CharField(max_length=200)
    mensaje         = models.TextField()
    fecha_envio     = models.DateTimeField(auto_now_add=True)
    fecha_evento    = models.DateField(null=True, blank=True)
    enviado_correo  = models.BooleanField(default=False)
    destinatarios   = models.ManyToManyField(Alumno, related_name='mensajes_recibidos', blank=True)

    class Meta:
        verbose_name        = 'Mensaje a Alumnos'
        verbose_name_plural = 'Mensajes a Alumnos'
        ordering            = ['-fecha_envio']

    def __str__(self):
        return f'{self.asunto} → {self.curso} ({self.fecha_envio:%d/%m/%Y})'
