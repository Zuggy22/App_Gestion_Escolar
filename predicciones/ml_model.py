# predicciones/ml_model.py
#
# Este archivo contiene el "cerebro" del sistema de predicción.
# Usamos un algoritmo llamado Random Forest que aprende de los datos
# existentes y predice el riesgo de nuevos alumnos.

import numpy as np
from sklearn.ensemble import RandomForestClassifier


def entrenar_modelo(alumnos):
    """
    Entrena el modelo con los datos de alumnos existentes.

    Recibe: queryset de alumnos desde la base de datos
    Retorna: modelo entrenado listo para predecir
    """

    # Si hay menos de 5 alumnos, usamos datos de ejemplo para entrenar
    datos_entrenamiento = [
        # [promedio, edad]  → etiqueta (0=sin riesgo, 1=en riesgo)
        [6.5, 15], [6.8, 16], [7.0, 15], [6.2, 17], [5.9, 15],
        [5.5, 16], [5.6, 14], [5.8, 15], [5.7, 16], [6.0, 17],
        [4.5, 15], [4.8, 16], [4.2, 17], [3.9, 15], [4.1, 16],
        [5.0, 14], [4.9, 15], [5.1, 16], [4.7, 17], [5.3, 15],
    ]
    etiquetas = [0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0,
                 1, 1, 1, 1, 1,
                 1, 1, 1, 1, 1]

    # Si hay suficientes alumnos reales, usamos sus datos
    if alumnos.count() >= 5:
        datos_entrenamiento = []
        etiquetas = []
        for alumno in alumnos:
            datos_entrenamiento.append([alumno.promedio, alumno.edad])
            etiquetas.append(1 if alumno.promedio < 5.5 else 0)

    X = np.array(datos_entrenamiento)
    y = np.array(etiquetas)

    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo.fit(X, y)
    return modelo


def predecir_riesgo(modelo, promedio, edad):
    """
    Predice si un alumno está en riesgo.

    Retorna un diccionario con:
    - en_riesgo: True/False
    - probabilidad: porcentaje de riesgo
    - nivel: 'Alto', 'Medio', 'Bajo'
    - color: color para mostrar en pantalla
    - mensaje: texto descriptivo
    """
    datos = np.array([[promedio, edad]])
    prediccion   = modelo.predict(datos)[0]
    probabilidad = modelo.predict_proba(datos)[0]

    # probabilidad[1] = probabilidad de estar en riesgo
    prob_riesgo = round(probabilidad[1] * 100, 1)

    if prob_riesgo >= 70:
        nivel   = 'Alto'
        color   = '#c0392b'
        emoji   = '🔴'
        mensaje = 'Requiere atención inmediata'
    elif prob_riesgo >= 40:
        nivel   = 'Medio'
        color   = '#f59e0b'
        emoji   = '🟡'
        mensaje = 'Seguimiento recomendado'
    else:
        nivel   = 'Bajo'
        color   = '#22c55e'
        emoji   = '🟢'
        mensaje = 'Rendimiento satisfactorio'

    return {
        'en_riesgo':    bool(prediccion),
        'probabilidad': prob_riesgo,
        'nivel':        nivel,
        'color':        color,
        'emoji':        emoji,
        'mensaje':      mensaje,
    }