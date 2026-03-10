from django import forms
from .models import Profesor

CAMPO = 'w-full px-4 py-2.5 border-2 border-slate-200 rounded-xl text-sm focus:outline-none focus:border-blue-500 transition'

ESPECIALIDADES = [
    ('', '-- Seleccionar --'),
    ('Matemáticas', 'Matemáticas'),
    ('Lenguaje',    'Lenguaje y Comunicación'),
    ('Ciencias',    'Ciencias Naturales'),
    ('Historia',    'Historia y Geografía'),
    ('Inglés',      'Inglés'),
    ('Educación Física', 'Educación Física'),
    ('Artes',       'Artes Visuales'),
    ('Otra',        'Otra'),
]

class ProfesorForm(forms.ModelForm):
    class Meta:
        model  = Profesor
        fields = ['nombre', 'especialidad', 'años_experiencia']
        widgets = {
            'nombre':           forms.TextInput(attrs={'class': CAMPO, 'placeholder': 'Ej: Ana Soto'}),
            'especialidad':     forms.Select(choices=ESPECIALIDADES, attrs={'class': CAMPO}),
            'años_experiencia': forms.NumberInput(attrs={'class': CAMPO, 'placeholder': 'Ej: 8'}),
        }