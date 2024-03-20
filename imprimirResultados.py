import numpy as np
from ganancias import obtener_ventas

def imprimir_resultados(
    resultado,
    lista_items_ordenados,
    lista_materiales_ordenados,
    presupuesto,
    precios_de_venta_items,
    cuota_de_creacion_por_unidad,
    precios_de_compra_materiales
):

    cantidad_items = resultado.x[:len(lista_items_ordenados)]
    cantidad_materiales = resultado.x[len(lista_items_ordenados):]
    ventas = obtener_ventas(precios_de_venta_items)
    ventas_totales = ventas @ cantidad_items
    cuotas_creacion = cuota_de_creacion_por_unidad @ cantidad_items
    compra_materiales = precios_de_compra_materiales @ cantidad_materiales

    print("\nCantidades óptimas:\n")
    print(f"  {"Objeto": <25} | {"Cantidad"} | {"Precio"}")
    print(f"  {"-":-<25}-|-{"-":-<8}-|-{"-":-<6}")
    for indice in np.where(resultado.x > 0.9)[0]:
        id_objeto = (lista_items_ordenados + lista_materiales_ordenados)[indice]
        cantidad_item = resultado.x[indice]
        precio_item = ventas[id_objeto] if indice < len(ventas) else precios_de_compra_materiales[indice - len(ventas)]

        print(f"  {id_objeto: <25} | {cantidad_item: <8.0f} | {precio_item/0.845: <6.0f}")

    print(f"\nPresupuesto inicial: {presupuesto}")
    print(f"Inversión: {cuotas_creacion + compra_materiales:.0f}")
    print(f"  Cuotas creación: {cuotas_creacion:.0f}")
    print(f"  Compra materiales: {compra_materiales:.0f}")
    print(f"Ventas totales: {ventas_totales:.0f}")
    print(f"Ganancia total: {-resultado.fun:.0f}")