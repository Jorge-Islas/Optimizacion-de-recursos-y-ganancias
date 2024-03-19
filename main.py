import numpy as np
from scipy.optimize import linprog
from cargarDatos import cargar_item_db
from restriccionesMateriales import obtener_resticciones_de_materiales
from restriccionDinero import obtener_restriccion_dinero
from Restricciones import obtener_restricciones
from llamadasAPI import obtener_precios
from ganancias import obtener_funcion_ganancias, obtener_ventas


import pandas as pd

item_db = cargar_item_db()

# Luego podrá cambiar esta lista con filtros y selecciones
# de objetos
lista_de_items = list(item_db.keys())

# lista_de_items = [
#     "T3_2H_TOOL_AXE",
#     "T3_2H_TOOL_HAMMER",
#     "T3_2H_TOOL_PICK",
#     "T3_2H_TOOL_SICKLE",
#     "T3_2H_TOOL_FISHINGROD"
# ]

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
    "Forja del guerrero": 2370,
    "Cabaña del cazador": 2360,
    "Torre del mago": 2370,
    "Fábrica de herramientas": 1150
}

# Presupuesto de dinero para la operación
presupuesto = 10000

# Ciudad donde se harán las operaciones
ciudad = "FortSterling"

# Usar api para obtener datos
usar_api = True

# Obtener restricciones de materiales y listas ordenadas
# de items y materiales
restricciones_de_materiales, lista_items_ordenados, lista_materiales_ordenados = obtener_resticciones_de_materiales(lista_de_items, materiales)

print(f"Items considerados: {len(lista_items_ordenados)}")
print(f"Materiales considerados: {len(lista_materiales_ordenados)}")

precios_de_venta_items, precios_de_compra_materiales = obtener_precios(
    lista_items_ordenados, lista_materiales_ordenados, ciudad, usar_api
)

df = pd.DataFrame({"items_ordenados": lista_items_ordenados, "items_precios": precios_de_venta_items.index, "precios": list(precios_de_venta_items)})

# Obtener restricción de dinero (costo no debe sobrepasar
# el presupuesto)
restriccion_de_dinero, cuota_de_creacion_por_unidad, precios_de_compra_materiales = obtener_restriccion_dinero(lista_items_ordenados, cuotas_de_estaciones, precios_de_compra_materiales)

matriz_restricciones, vector_restricciones = obtener_restricciones(
    restricciones_de_materiales,
    restriccion_de_dinero,
    presupuesto
)

# Obtener el vector de la función a optimizar
# (0.92 * ventas - cuotas_de_crafting) * cantidad_items
# - precios_de_compra_materiales * cantidad_materiales
funcion_ganancias = obtener_funcion_ganancias(
    precios_de_venta_items, cuota_de_creacion_por_unidad, precios_de_compra_materiales
)

# Resolver problema de programación lineal
c = -funcion_ganancias
A_ub = matriz_restricciones
b_ub = vector_restricciones

resultado = linprog(c, A_ub, b_ub, integrality=1, bounds=(0,None))

print("\nCantidades óptimas:")
for indice in np.where(resultado.x > 0.9)[0]:
    id_objeto = (lista_items_ordenados + lista_materiales_ordenados)[indice]
    cantidad_item = resultado.x[indice]
    print(f"  {id_objeto}: {cantidad_item}")

print(f"\nPresupuesto inicial: {presupuesto}")
cantidad_items = resultado.x[:len(lista_items_ordenados)]
cantidad_materiales = resultado.x[len(lista_items_ordenados):]
ventas = obtener_ventas(precios_de_venta_items) @ cantidad_items
cuotas_creacion = cuota_de_creacion_por_unidad @ cantidad_items
compra_materiales = precios_de_compra_materiales @ cantidad_materiales
print(f"Inversión: {cuotas_creacion + compra_materiales}")
print(f"  Cuotas creación: {cuotas_creacion}")
print(f"  Compra materiales: {compra_materiales}")
print(f"Ventas: {ventas}")
print(f"Ganancia total: {-resultado.fun}")
