import numpy as np
import pandas as pd

def obtener_ventas(precios_de_venta_items):
    coeficientes_de_venta = 0.895 * precios_de_venta_items
    return coeficientes_de_venta

def obtener_funcion_ganancias(
    precios_de_venta_items,
    cuota_de_creacion_por_unidad,
    precios_de_compra_materiales
):
    coeficientes_venta = obtener_ventas(precios_de_venta_items)
    coeficientes_items = coeficientes_venta - cuota_de_creacion_por_unidad
    coeficientes_de_funcion = np.hstack(
        (coeficientes_items, -precios_de_compra_materiales)
    )

    return coeficientes_de_funcion