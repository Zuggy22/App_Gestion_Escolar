# predicciones/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from alumnos.models import Alumno
from .ml_model import entrenar_modelo, predecir_riesgo


@login_required
def panel_predicciones(request):
    """
    Vista principal del módulo de Machine Learning.
    Analiza cada alumno y muestra su nivel de riesgo.
    """
    alumnos = Alumno.objects.all()

    # Entrenar el modelo con los datos actuales
    modelo = entrenar_modelo(alumnos)

    # Predecir riesgo para cada alumno
    resultados = []
    for alumno in alumnos:
        prediccion = predecir_riesgo(modelo, alumno.promedio, alumno.edad)
        resultados.append({
            'alumno':    alumno,
            'prediccion': prediccion,
        })

    # Ordenar: primero los de mayor riesgo
    resultados.sort(key=lambda x: x['prediccion']['probabilidad'], reverse=True)

    # Estadísticas generales
    en_riesgo  = sum(1 for r in resultados if r['prediccion']['en_riesgo'])
    sin_riesgo = len(resultados) - en_riesgo

    contexto = {
        'resultados':  resultados,
        'en_riesgo':   en_riesgo,
        'sin_riesgo':  sin_riesgo,
        'total':       len(resultados),
    }
    return render(request, 'predicciones/panel_predicciones.html', contexto)