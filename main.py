from scipy.optimize import linprog
from src.cargarDatos import cargar_item_db
from src.restricciones.restriccionesMateriales import obtener_resticciones_de_materiales
from src.restricciones.restriccionDinero import obtener_restriccion_dinero
from src.restricciones.Restricciones import obtener_restricciones
from src.llamadasAPI import obtener_precios
from src.ganancias import obtener_funcion_ganancias
from src.imprimirResultados import imprimir_resultados


import pandas as pd

item_db = cargar_item_db()

# Luego podrá cambiar esta lista con filtros y selecciones
# de objetos
registro_de_items = pd.DataFrame(list(item_db.values())).set_index("id").sort_index(axis=0)
# lista_de_items = registro_de_items[registro_de_items["nivel"] == 4].index
lista_de_items = registro_de_items.index

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
presupuesto = 100000

# Ciudad donde se harán las operaciones
ciudad = "FortSterling"

# Usar api para obtener datos
usar_api = False

# Obtener restricciones de materiales y listas ordenadas
# de items y materiales
restricciones_de_materiales, lista_items_ordenados, lista_materiales_ordenados = obtener_resticciones_de_materiales(lista_de_items, materiales)

print(f"Items considerados: {len(lista_items_ordenados)}")
print(f"Materiales considerados: {len(lista_materiales_ordenados)}")

precios_de_venta_items, precios_de_compra_materiales = obtener_precios(
    lista_items_ordenados, lista_materiales_ordenados, ciudad, usar_api
)

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

imprimir_resultados(
    resultado,
    lista_items_ordenados,
    lista_materiales_ordenados,
    presupuesto,
    precios_de_venta_items,
    cuota_de_creacion_por_unidad,
    precios_de_compra_materiales,
    item_db
)