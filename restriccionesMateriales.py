import pandas as pd
import numpy as np
from cargarDatos import cargar_item_db

def id_material_con_encantamiento(id_material, nivel, encantamiento):
    if encantamiento == 0:
        return f"T{nivel}_{id_material}"
    
    return f"T{nivel}_{id_material}_LEVEL{encantamiento}@{encantamiento}"

def obtener_resticciones_de_materiales(lista_items, materiales):
    item_db = cargar_item_db()

    materiales_requeridos_por_item = []

    for item in lista_items:
        info_item = item_db[item]
        nivel_item = info_item["nivel"]
        encantamiento_item = info_item["encantamiento"]
        
        materiales_requeridos = {"id": info_item["id"]}

        for material in list(materiales.keys()):
            id_material = materiales[material]
            id_material_final = id_material_con_encantamiento(
                id_material, nivel_item, encantamiento_item
            )

            materiales_requeridos[id_material_final] = info_item[material]
            
        materiales_requeridos_por_item.append(materiales_requeridos)
        

    tabla_materiales_requeridos = pd.DataFrame(materiales_requeridos_por_item).set_index("id").sort_index(axis=0).sort_index(axis=1).fillna(0)

    matriz_materiales_requeridos = np.transpose(np.array(tabla_materiales_requeridos.iloc[:,:]))

    restricciones_de_materiales = np.hstack((matriz_materiales_requeridos, -np.identity(tabla_materiales_requeridos.shape[1]))) # A_ub_0

    lista_items_ordenados = list(tabla_materiales_requeridos.index)
    lista_materiales_ordenados = list(tabla_materiales_requeridos.columns)
    
    return restricciones_de_materiales, lista_items_ordenados, lista_materiales_ordenados
