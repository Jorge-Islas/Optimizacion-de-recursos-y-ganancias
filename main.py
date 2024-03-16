import json
import pandas as pd
import numpy as np
from cargarDatos import cargar_item_db
from restriccionesMateriales import obtener_resticciones_de_materiales
from restriccionDinero import obtener_restriccion_dinero
from Restricciones import obtener_restricciones
from llamadasAPI import obtener_precios_compra_materiales, obtener_precios_venta_items
from ganancias import obtener_funcion_ganancias

item_db = cargar_item_db()

# Luego podrá cambiar esta lista con filtros y selecciones
# de objetos
lista_de_items = list(item_db.keys())
lista_de_items = [
    "T2_MAIN_SWORD",
    "T3_BAG",
    "T3_MAIN_CURSEDSTAFF"
]

# Despues importar la lista de materiales
# de algún otro lado
materiales = {
    "tablas": "PLANKS",
    "lingotes": "METALBAR",
    "tela": "CLOTH",
    "cuero": "LEATHER"
}
# El usuario llenará los campos de las cuotas de estaciones
# dados los objetos que eligió
cuotas_de_estaciones = {
    "Forja del guerrero": 2400,
    "Cabaña del cazador": 2390,
    "Torre del mago": 2360,
    "Fábrica de herramientas": 2120
}

# Presupuesto de dinero para la operación
presupuesto = 100000

# Ciudad donde se harán las operaciones
ciudad = "FortSterling"

# Obtener restricciones de materiales y listas ordenadas
# de items y materiales
restricciones_de_materiales, lista_items_ordenados, lista_materiales_ordenados = obtener_resticciones_de_materiales(lista_de_items, materiales)

precios_de_venta_items = obtener_precios_venta_items(
    lista_items_ordenados, ciudad
)
precios_de_compra_materiales = obtener_precios_compra_materiales(
    lista_materiales_ordenados, ciudad
)

# Obtener restricción de dinero (costo no debe sobrepasar
# el presupuesto)
restriccion_de_dinero, cuota_de_creacion_por_unidad, precios_de_compra_materiales = obtener_restriccion_dinero(lista_items_ordenados, cuotas_de_estaciones, precios_de_compra_materiales)

matriz_restricciones, vector_restricciones = obtener_restricciones(
    restricciones_de_materiales,
    restriccion_de_dinero,
    presupuesto
)

print(matriz_restricciones.shape)
print(vector_restricciones.shape)

# Obtener el vector de la función a optimizar
# (0.92 * ventas - cuotas_de_crafting) * cantidad_items
# - precios_de_compra_materiales * cantidad_materiales
funcion_ganancias = obtener_funcion_ganancias(
    precios_de_venta_items, cuota_de_creacion_por_unidad, precios_de_compra_materiales
)

print(funcion_ganancias.shape)

