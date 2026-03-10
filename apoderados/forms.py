from django import forms
from .models import Apoderado, MensajeApoderado

CAMPO = 'w-full px-4 py-2.5 rounded-lg text-sm outline-none transition input-elegant'


class ApoderadoForm(forms.ModelForm):
    class Meta:
        model  = Apoderado
        fields = ['alumno', 'nombre', 'rut', 'relacion', 'telefono',
                  'correo', 'direccion', 'datos_adicionales']
        widgets = {
            'alumno':    forms.Select(attrs={'class': CAMPO}),
            'nombre':    forms.TextInput(attrs={'class': CAMPO, 'placeholder': 'Nombre completo'}),
            'rut':       forms.TextInput(attrs={'class': CAMPO, 'placeholder': 'Ej: 12.345.678-9'}),
            'relacion':  forms.Select(attrs={'class': CAMPO}),
            'telefono':  forms.TextInput(attrs={'class': CAMPO, 'placeholder': 'Ej: +56 9 1234 5678'}),
            'correo':    forms.EmailInput(attrs={'class': CAMPO, 'placeholder': 'correo@ejemplo.com'}),
            'direccion': forms.TextInput(attrs={'class': CAMPO, 'placeholder': 'Calle, número, ciudad'}),
            'datos_adicionales': forms.Textarea(attrs={
                'class': CAMPO, 'rows': 3,
                'placeholder': 'Información adicional relevante...',
                'style': 'resize:vertical;'
            }),
        }
        labels = {
            'alumno':    'Alumno',
            'nombre':    'Nombre completo',
            'rut':       'RUT',
            'relacion':  'Relación con el alumno',
            'telefono':  'Teléfono',
            'correo':    'Correo electrónico',
            'direccion': 'Dirección',
            'datos_adicionales': 'Datos adicionales',
        }


class MensajeForm(forms.ModelForm):
    class Meta:
        model  = MensajeApoderado
        fields = ['categoria', 'asunto', 'mensaje']
        widgets = {
            'categoria': forms.Select(attrs={'class': CAMPO}),
            'asunto':    forms.TextInput(attrs={
                'class': CAMPO,
                'placeholder': 'Asunto del mensaje...'
            }),
            'mensaje':   forms.Textarea(attrs={
                'class': CAMPO, 'rows': 5,
                'placeholder': 'Escriba su mensaje al profesor jefe...',
                'style': 'resize:vertical;'
            }),
        }
        labels = {
            'categoria': 'Categoría',
            'asunto':    'Asunto',
            'mensaje':   'Mensaje',
        }


class RespuestaForm(forms.ModelForm):
    class Meta:
        model  = MensajeApoderado
        fields = ['respuesta', 'estado']
        widgets = {
            'respuesta': forms.Textarea(attrs={
                'class': CAMPO, 'rows': 4,
                'placeholder': 'Escriba su respuesta al apoderado...',
                'style': 'resize:vertical;'
            }),
            'estado': forms.Select(attrs={'class': CAMPO}),
        }
        labels = {
            'respuesta': 'Respuesta',
            'estado':    'Estado del mensaje',
        }