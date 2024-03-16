import numpy as np

def obtener_restricciones(
    restricciones_de_materiales,
    restriccion_de_dinero,
    presupuesto
):

    matriz_de_restricciones = np.vstack((
        restricciones_de_materiales,
        restriccion_de_dinero
    ))

    vector_de_restricciones = np.zeros(matriz_de_restricciones.shape[0])
    vector_de_restricciones[-1] = presupuesto

    return matriz_de_restricciones, vector_de_restricciones

