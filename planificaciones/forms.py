from django import forms
from .models import Planificacion, MensajeAlumno

CAMPO = 'w-full px-4 py-2.5 rounded-lg text-sm outline-none transition input-elegant'

ASIGNATURAS = [
    ('', '— Seleccionar —'),
    ('Lenguaje',         'Lenguaje'),
    ('Matemáticas',      'Matemáticas'),
    ('Ciencias',         'Ciencias'),
    ('Historia',         'Historia'),
    ('Inglés',           'Inglés'),
    ('Educación Física', 'Educación Física'),
    ('Artes',            'Artes'),
]


class PlanificacionForm(forms.ModelForm):
    class Meta:
        model  = Planificacion
        fields = ['tipo', 'curso', 'asignatura', 'fecha',
                  'unidad_tema', 'objetivos', 'actividades', 'recursos', 'estado']
        widgets = {
            'tipo':        forms.Select(attrs={'class': CAMPO}),
            'curso':       forms.TextInput(attrs={'class': CAMPO, 'placeholder': 'Ej: 1°A, 2°B...'}),
            'asignatura':  forms.Select(choices=ASIGNATURAS, attrs={'class': CAMPO}),
            'fecha':       forms.DateInput(attrs={'class': CAMPO, 'type': 'date'}),
            'unidad_tema': forms.TextInput(attrs={'class': CAMPO, 'placeholder': 'Ej: Unidad 2 — Fracciones'}),
            'objetivos':   forms.Textarea(attrs={'class': CAMPO, 'rows': 4,
                               'placeholder': 'Describe los objetivos de aprendizaje...'}),
            'actividades': forms.Textarea(attrs={'class': CAMPO, 'rows': 4,
                               'placeholder': 'Describe las actividades a realizar...'}),
            'recursos':    forms.Textarea(attrs={'class': CAMPO, 'rows': 3,
                               'placeholder': 'Materiales, libros, plataformas digitales... (opcional)'}),
            'estado':      forms.Select(attrs={'class': CAMPO}),
        }


class MensajeAlumnoForm(forms.ModelForm):
    class Meta:
        model  = MensajeAlumno
        fields = ['tipo', 'curso', 'asunto', 'mensaje', 'fecha_evento']
        widgets = {
            'tipo':         forms.Select(attrs={'class': CAMPO}),
            'curso':        forms.TextInput(attrs={'class': CAMPO, 'placeholder': 'Ej: 1°A o TODOS'}),
            'asunto':       forms.TextInput(attrs={'class': CAMPO, 'placeholder': 'Asunto del mensaje...'}),
            'mensaje':      forms.Textarea(attrs={'class': CAMPO, 'rows': 5,
                                'placeholder': 'Escribe el mensaje para los alumnos...'}),
            'fecha_evento': forms.DateInput(attrs={'class': CAMPO, 'type': 'date'}),
        }