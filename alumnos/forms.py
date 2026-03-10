from django import forms
from .models import Alumno

CAMPO = 'w-full px-4 py-2.5 border-2 border-slate-200 rounded-xl text-sm focus:outline-none focus:border-blue-500 transition'

class AlumnoForm(forms.ModelForm):
    class Meta:
        model  = Alumno
        fields = ['nombre', 'apellido', 'edad', 'correo', 'curso', 'promedio']
        widgets = {
            'nombre':   forms.TextInput(attrs={'class': CAMPO, 'placeholder': 'Ej: Valentina'}),
            'apellido': forms.TextInput(attrs={'class': CAMPO, 'placeholder': 'Ej: Rojas'}),
            'edad':     forms.NumberInput(attrs={'class': CAMPO, 'placeholder': 'Ej: 15'}),
            'correo':   forms.EmailInput(attrs={'class': CAMPO, 'placeholder': 'Ej: alumno@liceo.cl'}),
            'curso':    forms.TextInput(attrs={'class': CAMPO, 'placeholder': 'Ej: 1°A'}),
            'promedio': forms.NumberInput(attrs={'class': CAMPO, 'placeholder': 'Ej: 5.8'}),
        }