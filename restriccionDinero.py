import pandas as pd
import numpy as np
from cargarDatos import cargar_item_db

def obtener_restriccion_dinero(
    lista_items_ordenados,
    cuotas_de_estaciones: dict,
    precios_de_compra_materiales: dict
):
    item_db = cargar_item_db()

    registro_de_items = pd.DataFrame(list(item_db.values())).set_index("id").sort_index(axis=0)
    registro_de_items = registro_de_items.filter(items=lista_items_ordenados, axis=0)
    registro_de_items.loc[registro_de_items["nivel"] < 3, "valor"] = 0

    valor_de_item = registro_de_items["valor"]
    cuota_de_estacion = registro_de_items["estacion"].map(cuotas_de_estaciones)
    cuota_de_creacion_por_unidad = np.array(valor_de_item * 0.1125 * cuota_de_estacion * 0.01)

    precios_de_compra_materiales = np.array(pd.Series(precios_de_compra_materiales).sort_index())
    
    restriccion_de_dinero = np.hstack(
        (cuota_de_creacion_por_unidad, precios_de_compra_materiales)
    )
    
    return restriccion_de_dinero
