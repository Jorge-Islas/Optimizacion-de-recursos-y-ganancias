import requests
import json
import pandas as pd
import numpy as np

# API endpoint for Albion Online Data Project
ALBION_DATA_URL = "https://west.albion-online-data.com/api/v2/stats/prices/"

def dar_formato_url(
    lista_de_objetos, 
    ciudad, 
    calidades
):
    return ALBION_DATA_URL + ",".join(lista_de_objetos) + ".json?locations="+ciudad+"&qualities=" + ",".join([str(calidad) for calidad in calidades])

def obtener_respuesta_API(
    lista_de_objetos,
    ciudad,
    calidades=[1,2,3]
):
    url = dar_formato_url(
        lista_de_objetos, ciudad, calidades
    )
    respuesta = requests.get(url).json()

    return respuesta

def procesar_datos_items(datos_api_items):
    datos_api_items = pd.DataFrame(datos_api_items)
    datos_api_items["item_id"] = datos_api_items["item_id"].str.upper()

    datos_api_items = datos_api_items.set_index("item_id").sort_index(axis=0)["buy_price_max"].replace(0, np.nan)

    # Agrupar y obtener promedio sin contar ceros
    datos_api_items = datos_api_items.groupby("item_id").mean()

    datos_faltantes = datos_api_items[datos_api_items.isna()].index

    for item in datos_faltantes:
        datos_api_items[item] = int(input(f"Precio de venta {item}: "))
    
    return datos_api_items

def procesar_datos_materiales(datos_api_materiales):
    datos_api_materiales = pd.DataFrame(datos_api_materiales)
    datos_api_materiales["item_id"] = datos_api_materiales["item_id"].str.upper()

    datos_api_materiales = datos_api_materiales.set_index("item_id").sort_index(axis=0)["sell_price_min"].replace(0, np.nan)

    datos_faltantes = datos_api_materiales[datos_api_materiales.isna()].index

    for item in datos_faltantes:
        datos_api_materiales[item] = int(input(f"Precio de compra {item}: "))

    return datos_api_materiales

def obtener_precios(
    lista_items_ordenados: list,
    lista_materiales_ordenados: list,
    ciudad: str,
    usar_api=True
) -> pd.Series:
    datos_mercado_albion = None

    if not usar_api:
        # Cargar archivos json
        try:
            with open("datos-api-items.json", "r") as file:
                datos_api_materiales = json.load(file)

            with open("datos-api-materiales.json", "r") as file:
                datos_api_materiales = json.load(file)

        except Exception as e:
            print(f"ERROR: {e}")
            print("\nUsando API para descargar datos más recientes...")
    
    if datos_mercado_albion is None:
        # Usar API
        datos_api_items = obtener_respuesta_API(
            lista_items_ordenados, ciudad
        )
        datos_api_materiales = obtener_respuesta_API(
            lista_materiales_ordenados, ciudad, calidades=[0]
        )
        # Guardar datos en archivos json
        with open("datos-api-items.json", "w") as file:
            json.dump(datos_api_items, file)

        with open("datos-api-materiales.json", "w") as file:
            json.dump(datos_api_materiales, file)

    precios_venta_items = procesar_datos_items(datos_api_items)
    precios_compra_materiales = procesar_datos_materiales(datos_api_materiales)

    # Return provisional
    return precios_venta_items, precios_compra_materiales
