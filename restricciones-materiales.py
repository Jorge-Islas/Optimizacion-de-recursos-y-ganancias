import json
import pandas as pd
import numpy as np

# Despues importar de algún lado
materials = {
    "tablas": "PLANKS",
    "lingotes": "METALBAR",
    "tela": "CLOTH",
    "cuero": "LEATHER"
}

def cargar_item_db():
    with open("item-db.json", "r") as file:
        item_db = json.load(file)
    return item_db

def material_string_id(material_id, tier, enchantment):
    if enchantment == 0:
        return f"T{tier}_{material_id}"
    
    return f"T{tier}_{material_id}_LEVEL{enchantment}@{enchantment}"

def obtener_resticciones_de_materiales(item_list=None):
    item_db = cargar_item_db()

    # Luego podrá cambiar esta lista
    item_list = list(item_db.keys())

    item_material_requirements = []

    for item in item_list:
        item_info = item_db[item]
        item_tier = item_info["nivel"]
        item_enchantment = item_info["encantamiento"]
        
        material_requirements = {"id": item_info["id"]}

        for material in list(materials.keys()):
            material_id = materials[material]
            material_str_id = material_string_id(
                material_id, item_tier, item_enchantment
            )

            material_requirements[material_str_id] = item_info[material]
            
        item_material_requirements.append(material_requirements)
        

    df = pd.DataFrame(item_material_requirements).set_index("id").sort_index(axis=0).sort_index(axis=1).fillna(0)

    df_as_matrix = np.transpose(np.array(df.iloc[:,:]))
    A_ub_0 = np.hstack((df_as_matrix, -np.identity(df.shape[1])))

    
    return A_ub_0, list(df.index), list(df.columns)

mtx, idx, cols = obtener_resticciones_de_materiales()
print(idx)
print(cols)