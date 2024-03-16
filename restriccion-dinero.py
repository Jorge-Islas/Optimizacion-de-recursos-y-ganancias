import json
import pandas as pd
import numpy as np

# ---- Funcion duplicada ----
def cargar_item_db():
    with open("item-db.json", "r") as file:
        item_db = json.load(file)
    return item_db

def obtener_restriccion_dinero(
    item_list_sorted,
    cuotas_de_estaciones: dict,
    material_sell_prices: dict
):
    item_db = cargar_item_db()

    df = pd.DataFrame(list(item_db.values())).set_index("id").sort_index(axis=0)
    df = df[df["id"].isin(item_list_sorted)]
    df.loc[df["nivel"] < 3, "valor"] = 0

    item_value = df["valor"]
    item_sation_fee = df["estacion"].map(cuotas_de_estaciones)
    item_crafting_fee_per_unit = np.array(item_value * 0.1125 * item_sation_fee * 0.01)

    material_sell_prices = np.array(pd.Series(material_sell_prices).sort_index())
    
    A_ub_1 = np.hstack(
        (item_crafting_fee_per_unit, material_sell_prices)
    )
    
    return A_ub_1

cuotas_de_estaciones = {
    "Forja del guerrero": 2400,
    "Cabaña del cazador": 2390,
    "Torre del mago": 2360,
    "Fábrica de herramientas": 2120
}
material_sell_prices = {
    "T2_PLANKS": 12,
    "T2_METALBARS": 12,
    "T2_CLOTH": 12,
    "T2_LEATHER": 12,
    "T3_PLANKS": 24,
    "T3_METALBARS": 24,
    "T3_CLOTH": 24,
    "T3_LEATHER": 24,
}
obtener_restriccion_dinero([], cuotas_de_estaciones, material_sell_prices)