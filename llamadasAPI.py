import requests
import json
import pandas as pd

def obtener_precios_venta_items(
    lista_items_ordenados: list,
    ciudad: str
) -> pd.Series:
    # En el futuro esto se obtendrá con la API de 
    # Albion Online Data Project
    return pd.Series({
        item: 500 for item in lista_items_ordenados
    })

def obtener_precios_compra_materiales(
    lista_materiales_ordenados,
    ciudad: str
):
    # Esto se conseguirá por medio de la API y / o
    # de lo que ingrese el usuario a partir de
    # -- lista_materiales_ordenados --
    return {
        material: 12 if '2' in material else 3 for material in lista_materiales_ordenados
    }