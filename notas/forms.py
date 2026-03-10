# notas/forms.py
from django import forms
from .models import Nota, Asistencia, ASIGNATURAS, Observacion

import datetime

CAMPO = 'w-full px-4 py-2.5 rounded-lg text-sm outline-none transition input-elegant'


class NotaForm(forms.ModelForm):
    class Meta:
        model  = Nota
        fields = ['asignatura', 'nota_1', 'nota_2', 'nota_3', 'nota_4']
        widgets = {
            'asignatura': forms.Select(attrs={'class': CAMPO}),
            'nota_1': forms.NumberInput(attrs={
                'class': CAMPO, 'placeholder': 'Ej: 5.5',
                'step': '0.1', 'min': '1.0', 'max': '7.0'
            }),
            'nota_2': forms.NumberInput(attrs={
                'class': CAMPO, 'placeholder': 'Ej: 6.0',
                'step': '0.1', 'min': '1.0', 'max': '7.0'
            }),
            'nota_3': forms.NumberInput(attrs={
                'class': CAMPO, 'placeholder': 'Ej: 6.5',
                'step': '0.1', 'min': '1.0', 'max': '7.0'
            }),
            'nota_4': forms.NumberInput(attrs={
                'class': CAMPO, 'placeholder': 'Ej: 7.0',
                'step': '0.1', 'min': '1.0', 'max': '7.0'
            }),
        }
        labels = {
            'asignatura': 'Asignatura',
            'nota_1':     'Nota 1',
            'nota_2':     'Nota 2',
            'nota_3':     'Nota 3',
            'nota_4':     'Nota 4',
        }

    def clean(self):
        cleaned_data = super().clean()
        for campo in ['nota_1', 'nota_2', 'nota_3', 'nota_4']:
            nota = cleaned_data.get(campo)
            if nota is not None:
                if nota < 1.0 or nota > 7.0:
                    self.add_error(campo, 'La nota debe estar entre 1.0 y 7.0')
        return cleaned_data


class AsistenciaForm(forms.ModelForm):
    class Meta:
        model  = Asistencia
        fields = ['asignatura', 'fecha', 'estado']
        widgets = {
            'asignatura': forms.Select(attrs={'class': CAMPO}),
            'fecha': forms.DateInput(attrs={
                'class': CAMPO,
                'type':  'date',
                'max':   datetime.date.today().strftime('%Y-%m-%d'),
            }),
            'estado': forms.Select(attrs={'class': CAMPO}),
        }
        labels = {
            'asignatura': 'Asignatura',
            'fecha':      'Fecha de clase',
            'estado':     'Estado de asistencia',
        }

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        if fecha and fecha.weekday() >= 5:
            raise forms.ValidationError(
                '⚠️ Solo se puede registrar asistencia de Lunes a Viernes.'
            )
        return fecha


class AsistenciaMasivaForm(forms.Form):
    asignatura = forms.ChoiceField(
        choices=ASIGNATURAS,
        widget=forms.Select(attrs={'class': CAMPO})
    )
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': CAMPO,
            'type':  'date',
            'max':   datetime.date.today().strftime('%Y-%m-%d'),
        })
    )

class ObservacionForm(forms.ModelForm):
    class Meta:
        model  = Observacion
        fields = ['categoria', 'texto']
        widgets = {
            'categoria': forms.Select(attrs={'class': CAMPO}),
            'texto': forms.Textarea(attrs={
                'class': CAMPO,
                'rows':  4,
                'placeholder': 'Escriba aquí la observación del alumno...',
                'style': 'resize:vertical;',
            }),
        }
        labels = {
            'categoria': 'Categoría',
            'texto':     'Observación',
        }