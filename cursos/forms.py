from django import forms
from .models import Curso

CAMPO = 'w-full px-4 py-2.5 border-2 border-slate-200 rounded-xl text-sm focus:outline-none focus:border-blue-500 transition'

class CursoForm(forms.ModelForm):
    class Meta:
        model  = Curso
        fields = ['nombre_ramo', 'nivel', 'jornada', 'profesor_jefe']
        widgets = {
            'nombre_ramo':   forms.TextInput(attrs={'class': CAMPO, 'placeholder': 'Ej: Matemáticas 1°A'}),
            'nivel':         forms.Select(attrs={'class': CAMPO}),
            'jornada':       forms.Select(attrs={'class': CAMPO}),
            'profesor_jefe': forms.Select(attrs={'class': CAMPO}),
        }