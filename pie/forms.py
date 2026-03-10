from django import forms
from .models import RegistroPIE, Especialista, PACI, EvaluacionPIE, InformeAvance

CAMPO = 'w-full px-4 py-2.5 rounded-lg text-sm outline-none transition input-elegant'
AREA  = 'w-full px-4 py-2.5 rounded-lg text-sm outline-none transition input-elegant'


class RegistroPIEForm(forms.ModelForm):
    class Meta:
        model  = RegistroPIE
        fields = ['alumno', 'necesidad', 'nivel_apoyo',
                  'fecha_ingreso', 'diagnostico', 'observaciones', 'activo']
        widgets = {
            'alumno':        forms.Select(attrs={'class': CAMPO}),
            'necesidad':     forms.Select(attrs={'class': CAMPO}),
            'nivel_apoyo':   forms.Select(attrs={'class': CAMPO}),
            'fecha_ingreso': forms.DateInput(attrs={'class': CAMPO, 'type': 'date'}),
            'diagnostico':   forms.Textarea(attrs={'class': AREA, 'rows': 4,
                                 'placeholder': 'Describe el diagnóstico clínico del alumno...'}),
            'observaciones': forms.Textarea(attrs={'class': AREA, 'rows': 3,
                                 'placeholder': 'Observaciones adicionales (opcional)...'}),
            'activo':        forms.CheckboxInput(attrs={'class': 'w-4 h-4 accent-yellow-400'}),
        }


class EspecialistaForm(forms.ModelForm):
    class Meta:
        model  = Especialista
        fields = ['especialidad', 'nombre', 'correo', 'telefono',
                  'dias', 'hora_inicio', 'hora_fin', 'observaciones']
        widgets = {
            'especialidad': forms.Select(attrs={'class': CAMPO}),
            'nombre':       forms.TextInput(attrs={'class': CAMPO,
                                'placeholder': 'Nombre completo del especialista'}),
            'correo':       forms.EmailInput(attrs={'class': CAMPO,
                                'placeholder': 'correo@ejemplo.com'}),
            'telefono':     forms.TextInput(attrs={'class': CAMPO,
                                'placeholder': '+56 9 ...'}),
            'dias':         forms.TextInput(attrs={'class': CAMPO,
                                'placeholder': 'lunes,miercoles,viernes'}),
            'hora_inicio':  forms.TimeInput(attrs={'class': CAMPO, 'type': 'time'}),
            'hora_fin':     forms.TimeInput(attrs={'class': CAMPO, 'type': 'time'}),
            'observaciones':forms.Textarea(attrs={'class': AREA, 'rows': 2,
                                'placeholder': 'Observaciones (opcional)'}),
        }


class PACIForm(forms.ModelForm):
    class Meta:
        model  = PACI
        fields = ['anno', 'trimestre', 'asignatura', 'objetivo_general',
                  'objetivos_especificos', 'estrategias', 'recursos', 'responsable']
        widgets = {
            'anno':                   forms.NumberInput(attrs={'class': CAMPO,
                                          'placeholder': '2025'}),
            'trimestre':              forms.Select(attrs={'class': CAMPO}),
            'asignatura':             forms.TextInput(attrs={'class': CAMPO,
                                          'placeholder': 'Ej: Matemáticas'}),
            'objetivo_general':       forms.Textarea(attrs={'class': AREA, 'rows': 3,
                                          'placeholder': 'Objetivo general del plan...'}),
            'objetivos_especificos':  forms.Textarea(attrs={'class': AREA, 'rows': 4,
                                          'placeholder': 'Lista los objetivos específicos...'}),
            'estrategias':            forms.Textarea(attrs={'class': AREA, 'rows': 4,
                                          'placeholder': 'Estrategias metodológicas a utilizar...'}),
            'recursos':               forms.Textarea(attrs={'class': AREA, 'rows': 2,
                                          'placeholder': 'Materiales y recursos (opcional)'}),
            'responsable':            forms.TextInput(attrs={'class': CAMPO,
                                          'placeholder': 'Nombre del responsable'}),
        }


class EvaluacionPIEForm(forms.ModelForm):
    class Meta:
        model  = EvaluacionPIE
        fields = ['tipo', 'asignatura', 'especialista', 'fecha',
                  'descripcion', 'adecuaciones', 'nota_obtenida', 'observaciones']
        widgets = {
            'tipo':          forms.Select(attrs={'class': CAMPO}),
            'asignatura':    forms.TextInput(attrs={'class': CAMPO,
                                 'placeholder': 'Ej: Lenguaje'}),
            'especialista':  forms.Select(attrs={'class': CAMPO}),
            'fecha':         forms.DateInput(attrs={'class': CAMPO, 'type': 'date'}),
            'descripcion':   forms.Textarea(attrs={'class': AREA, 'rows': 3,
                                 'placeholder': 'Describe la evaluación realizada...'}),
            'adecuaciones':  forms.Textarea(attrs={'class': AREA, 'rows': 3,
                                 'placeholder': 'Ej: tiempo extendido, lectura en voz alta...'}),
            'nota_obtenida': forms.NumberInput(attrs={'class': CAMPO,
                                 'placeholder': '1.0 – 7.0', 'step': '0.1',
                                 'min': '1.0', 'max': '7.0'}),
            'observaciones': forms.Textarea(attrs={'class': AREA, 'rows': 2,
                                 'placeholder': 'Observaciones adicionales (opcional)'}),
        }


class InformeAvanceForm(forms.ModelForm):
    class Meta:
        model  = InformeAvance
        fields = ['anno', 'trimestre', 'especialista', 'logros',
                  'dificultades', 'sugerencias', 'para_apoderado']
        widgets = {
            'anno':           forms.NumberInput(attrs={'class': CAMPO,
                                  'placeholder': '2025'}),
            'trimestre':      forms.Select(attrs={'class': CAMPO}),
            'especialista':   forms.Select(attrs={'class': CAMPO}),
            'logros':         forms.Textarea(attrs={'class': AREA, 'rows': 4,
                                  'placeholder': 'Describe los logros alcanzados...'}),
            'dificultades':   forms.Textarea(attrs={'class': AREA, 'rows': 3,
                                  'placeholder': 'Dificultades observadas en el período...'}),
            'sugerencias':    forms.Textarea(attrs={'class': AREA, 'rows': 3,
                                  'placeholder': 'Recomendaciones y próximos objetivos...'}),
            'para_apoderado': forms.Textarea(attrs={'class': AREA, 'rows': 4,
                                  'placeholder': 'Mensaje en lenguaje simple para la familia...'}),
        }