from django.db import models
from alumnos.models import Alumno


# ── Catálogos ─────────────────────────────────────────────

NECESIDADES = [
    ('TEA',   '🧩 TEA — Trastorno del Espectro Autista'),
    ('TDAH',  '⚡ TDAH — Déficit Atencional e Hiperactividad'),
    ('DEA',   '📖 DEA — Dificultad Específica del Aprendizaje'),
    ('DI',    '🧠 DI — Discapacidad Intelectual'),
    ('DL',    '🗣️ DL — Dificultad del Lenguaje'),
    ('DM',    '♿ DM — Discapacidad Motora'),
    ('DV',    '👁️ DV — Discapacidad Visual'),
    ('DA',    '👂 DA — Discapacidad Auditiva'),
    ('OTRO',  '📋 Otro'),
]

NIVELES_APOYO = [
    ('leve',     '🟢 Leve'),
    ('moderado', '🟡 Moderado'),
    ('severo',   '🔴 Severo'),
]

ESPECIALIDADES = [
    ('psicologo',       '🧠 Psicólogo/a'),
    ('fonoaudiologo',   '🗣️ Fonoaudiólogo/a'),
    ('t_ocupacional',   '🤝 Terapeuta Ocupacional'),
    ('prof_diferencial','📚 Profesor/a Diferencial'),
    ('asist_social',    '👥 Asistente Social'),
]

DIAS = [
    ('lunes',     'Lunes'),
    ('martes',    'Martes'),
    ('miercoles', 'Miércoles'),
    ('jueves',    'Jueves'),
    ('viernes',   'Viernes'),
]

TRIMESTRES = [
    ('1', '1er Trimestre'),
    ('2', '2do Trimestre'),
    ('3', '3er Trimestre'),
]


# ── Modelo principal: Registro PIE ───────────────────────

class RegistroPIE(models.Model):
    alumno              = models.OneToOneField(
        Alumno, on_delete=models.CASCADE, related_name='pie'
    )
    necesidad           = models.CharField(max_length=10, choices=NECESIDADES)
    nivel_apoyo         = models.CharField(max_length=10, choices=NIVELES_APOYO)
    fecha_ingreso       = models.DateField()
    diagnostico         = models.TextField(
        verbose_name='Descripción del diagnóstico'
    )
    observaciones       = models.TextField(blank=True)
    activo              = models.BooleanField(default=True)
    fecha_registro      = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = 'Registro PIE'
        verbose_name_plural = 'Registros PIE'
        ordering            = ['alumno__apellido']

    def __str__(self):
        return f'{self.alumno} — {self.get_necesidad_display()}'

    def color_nivel(self):
        c = {
            'leve':     {'bg': 'rgba(34,197,94,0.12)',  'border': 'rgba(34,197,94,0.3)',  'text': '#86efac'},
            'moderado': {'bg': 'rgba(234,179,8,0.12)',  'border': 'rgba(234,179,8,0.3)',  'text': '#fde68a'},
            'severo':   {'bg': 'rgba(239,68,68,0.12)',  'border': 'rgba(239,68,68,0.3)',  'text': '#fca5a5'},
        }
        return c.get(self.nivel_apoyo, c['leve'])


# ── Especialista asignado ────────────────────────────────

class Especialista(models.Model):
    registro        = models.ForeignKey(
        RegistroPIE, on_delete=models.CASCADE, related_name='especialistas'
    )
    especialidad    = models.CharField(max_length=20, choices=ESPECIALIDADES)
    nombre          = models.CharField(max_length=150)
    correo          = models.EmailField(blank=True)
    telefono        = models.CharField(max_length=20, blank=True)
    dias            = models.CharField(
        max_length=100,
        help_text='Días separados por coma: lunes,miercoles'
    )
    hora_inicio     = models.TimeField()
    hora_fin        = models.TimeField()
    observaciones   = models.TextField(blank=True)

    class Meta:
        verbose_name        = 'Especialista'
        verbose_name_plural = 'Especialistas'

    def __str__(self):
        return f'{self.get_especialidad_display()} — {self.nombre}'

    def dias_lista(self):
        return [d.strip().capitalize() for d in self.dias.split(',') if d.strip()]

    def horas_formato(self):
        return f'{self.hora_inicio.strftime("%H:%M")} – {self.hora_fin.strftime("%H:%M")}'


# ── PACI — Plan de Adecuación Curricular Individual ──────

class PACI(models.Model):
    registro            = models.ForeignKey(
        RegistroPIE, on_delete=models.CASCADE, related_name='pacis'
    )
    anno                = models.IntegerField(verbose_name='Año')
    trimestre           = models.CharField(max_length=1, choices=TRIMESTRES)
    asignatura          = models.CharField(max_length=100)
    objetivo_general    = models.TextField()
    objetivos_especificos = models.TextField()
    estrategias         = models.TextField()
    recursos            = models.TextField(blank=True)
    responsable         = models.CharField(max_length=150)
    fecha_creacion      = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = 'PACI'
        verbose_name_plural = 'PACIs'
        ordering            = ['-anno', 'trimestre']
        unique_together     = ['registro', 'anno', 'trimestre', 'asignatura']

    def __str__(self):
        return f'PACI {self.anno} T{self.trimestre} — {self.asignatura}'


# ── Evaluación diferenciada ──────────────────────────────

class EvaluacionPIE(models.Model):
    TIPOS_EVAL = [
        ('prueba',      '📝 Prueba Diferenciada'),
        ('trabajo',     '📋 Trabajo Diferenciado'),
        ('oral',        '🗣️ Evaluación Oral'),
        ('portafolio',  '📁 Portafolio'),
        ('otro',        '📌 Otro'),
    ]

    registro        = models.ForeignKey(
        RegistroPIE, on_delete=models.CASCADE, related_name='evaluaciones'
    )
    especialista    = models.ForeignKey(
        Especialista, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='evaluaciones'
    )
    tipo            = models.CharField(max_length=15, choices=TIPOS_EVAL)
    asignatura      = models.CharField(max_length=100)
    fecha           = models.DateField()
    descripcion     = models.TextField()
    adecuaciones    = models.TextField(
        verbose_name='Adecuaciones aplicadas',
        help_text='Describe qué adecuaciones se realizaron para esta evaluación'
    )
    nota_obtenida   = models.DecimalField(
        max_digits=3, decimal_places=1,
        null=True, blank=True
    )
    observaciones   = models.TextField(blank=True)
    fecha_registro  = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = 'Evaluación PIE'
        verbose_name_plural = 'Evaluaciones PIE'
        ordering            = ['-fecha']

    def __str__(self):
        return f'{self.get_tipo_display()} — {self.asignatura} — {self.fecha}'

    def color_nota(self):
        if self.nota_obtenida is None:
            return '#475569'
        n = float(self.nota_obtenida)
        if n >= 5.5:
            return '#86efac'
        elif n >= 4.5:
            return '#fde68a'
        return '#fca5a5'


# ── Informe de avance ────────────────────────────────────

class InformeAvance(models.Model):
    registro        = models.ForeignKey(
        RegistroPIE, on_delete=models.CASCADE, related_name='informes'
    )
    anno            = models.IntegerField(verbose_name='Año')
    trimestre       = models.CharField(max_length=1, choices=TRIMESTRES)
    especialista    = models.ForeignKey(
        Especialista, on_delete=models.SET_NULL,
        null=True, blank=True
    )
    logros          = models.TextField(verbose_name='Logros del período')
    dificultades    = models.TextField(verbose_name='Dificultades observadas')
    sugerencias     = models.TextField(verbose_name='Sugerencias y próximos pasos')
    para_apoderado  = models.TextField(
        verbose_name='Mensaje para el apoderado',
        help_text='Texto en lenguaje simple para compartir con la familia'
    )
    fecha_emision   = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name        = 'Informe de Avance'
        verbose_name_plural = 'Informes de Avance'
        ordering            = ['-anno', 'trimestre']

    def __str__(self):
        return f'Informe {self.anno} T{self.trimestre} — {self.registro.alumno}'