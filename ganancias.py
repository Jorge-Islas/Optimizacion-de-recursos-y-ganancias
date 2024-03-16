import numpy as np
import pandas as pd

def obtener_funcion_ganancias(
    precios_de_venta_items,
    cuota_de_creacion_por_unidad,
    precios_de_compra_materiales
):
    coeficientes_items = 0.92 * precios_de_venta_items - cuota_de_creacion_por_unidad
    coeficientes_de_funcion = np.hstack(
        (coeficientes_items, -precios_de_compra_materiales)
    )

    return coeficientes_de_funcion