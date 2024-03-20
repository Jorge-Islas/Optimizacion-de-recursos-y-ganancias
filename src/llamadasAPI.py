import requests
import pandas as pd
import numpy as np

# API endpoint for Albion Online Data Project
ALBION_DATA_URL = "https://west.albion-online-data.com/api/v2/stats/prices/"

def cargar_archivos_csv():
    # Cargar archivos csv
    try:
        precios_venta_items = pd.read_csv(
            "datos/precios-api-items.csv",
            header=0,
            index_col="item_id"
        )["sell_price_min"]

        precios_compra_materiales = pd.read_csv(
            "datos/precios-api-materiales.csv",
            header=0,
            index_col="item_id"
        )["sell_price_min"]
    
    except Exception as e:
        print(f"ERROR: {e}")
        print("\nUsando API para descargar datos más recientes...")
    
    return precios_venta_items, precios_compra_materiales

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

    datos_api_items = datos_api_items.set_index("item_id").sort_index(axis=0)["sell_price_min"].replace(0, np.nan)

    # Agrupar y obtener promedio sin contar ceros
    datos_api_items = datos_api_items.groupby("item_id").mean()

    datos_faltantes = datos_api_items[datos_api_items.isna()].index

    for item in datos_faltantes:
        datos_api_items[item] = int(input(f"Precio de venta {item}: "))
    
    precios_con_impuestos = (1 - 0.025 - 0.05) * datos_api_items
    #                            orden   precio
    #                          de venta  competitivo

    return precios_con_impuestos

def procesar_datos_materiales(datos_api_materiales):
    datos_api_materiales = pd.DataFrame(datos_api_materiales)
    datos_api_materiales["item_id"] = datos_api_materiales["item_id"].str.upper()

    datos_api_materiales = datos_api_materiales.set_index("item_id").sort_index(axis=0)["sell_price_min"].replace(0, np.nan)

    datos_faltantes = datos_api_materiales[datos_api_materiales.isna()].index

    for item in datos_faltantes:
        datos_api_materiales[item] = int(input(f"Precio de compra {item}: "))

    precios_con_margen_error = (1 + 0.1) * datos_api_materiales
    #                              precios
    #                              inflados

    return precios_con_margen_error

def obtener_datos_api(
    lista_items_ordenados,
    lista_materiales_ordenados,
    ciudad
):
    # Usar API
    datos_api_items = obtener_respuesta_API(
        lista_items_ordenados, ciudad
    )
    datos_api_materiales = obtener_respuesta_API(
        lista_materiales_ordenados, ciudad, calidades=[0]
    )

    precios_venta_items = procesar_datos_items(datos_api_items)
    precios_compra_materiales = procesar_datos_materiales(datos_api_materiales)

    precios_venta_items.to_csv("datos/precios-api-items.csv")
    precios_compra_materiales.to_csv("datos/precios-api-materiales.csv")

    return precios_venta_items, precios_compra_materiales

def obtener_precios(
    lista_items_ordenados: list,
    lista_materiales_ordenados: list,
    ciudad: str,
    usar_api=True
) -> pd.Series:
    
    precios_venta_items = None
    precios_compra_materiales = None

    if not usar_api:
        precios_venta_items, precios_compra_materiales = cargar_archivos_csv()
    
    if precios_venta_items is None or precios_compra_materiales is None:
        precios_venta_items, precios_compra_materiales = obtener_datos_api(
            lista_items_ordenados,
            lista_materiales_ordenados,
            ciudad
        )

    precios_venta_items = precios_venta_items.loc[lista_items_ordenados]
    
    precios_compra_materiales = precios_compra_materiales.loc[lista_materiales_ordenados]

    return precios_venta_items, precios_compra_materiales
