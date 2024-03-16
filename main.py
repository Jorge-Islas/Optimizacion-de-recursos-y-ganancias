import json
import pandas as pd
import numpy as np
from cargarDatos import cargar_item_db
from restriccionesMateriales import obtener_resticciones_de_materiales
from restriccionDinero import obtener_restriccion_dinero
from Restricciones import obtener_restricciones

item_db = cargar_item_db()

# Luego podrá cambiar esta lista con filtros y selecciones
# de objetos
lista_de_items = list(item_db.keys())

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

# Obtener restricciones de materiales y listas ordenadas
# de items y materiales
restricciones_de_materiales, lista_items_ordenados, lista_materiales_ordenados = obtener_resticciones_de_materiales(lista_de_items, materiales)

# Esto se conseguirá por medio de la API y / o
# de lo que ingrese el usuario a partir de
# -- lista_materiales_ordenados --
precios_de_compra_materiales = {
    "T2_PLANKS": 12,
    "T2_METALBARS": 12,
    "T2_CLOTH": 12,
    "T2_LEATHER": 12,
    "T3_PLANKS": 24,
    "T3_METALBARS": 24,
    "T3_CLOTH": 24,
    "T3_LEATHER": 24,
}

# Obtener restricción de dinero (costo no debe sobrepasar
# el presupuesto)
restriccion_de_dinero = obtener_restriccion_dinero(lista_items_ordenados, cuotas_de_estaciones, precios_de_compra_materiales)

matriz_restricciones, vector_restricciones = obtener_restricciones(
    restricciones_de_materiales,
    restriccion_de_dinero,
    presupuesto
)

print(matriz_restricciones.shape)
print(vector_restricciones.shape)