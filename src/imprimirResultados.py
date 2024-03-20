import numpy as np
from src.ganancias import obtener_ventas

def imprimir_resultados(
    resultado,
    lista_items_ordenados,
    lista_materiales_ordenados,
    presupuesto,
    precios_de_venta_items,
    cuota_de_creacion_por_unidad,
    precios_de_compra_materiales,
    item_db
):

    cantidad_items = resultado.x[:len(lista_items_ordenados)]
    cantidad_materiales = resultado.x[len(lista_items_ordenados):]
    ventas = obtener_ventas(precios_de_venta_items)
    ventas_totales = ventas @ cantidad_items
    cuotas_creacion = cuota_de_creacion_por_unidad @ cantidad_items
    compra_materiales = precios_de_compra_materiales @ cantidad_materiales

    print("\nCantidades óptimas:\n")
    print(f"  {"ID Objeto": <25} | {"Nombre Objeto": <30} | {"Cantidad"} | {"Precio"}")
    print(f"  {"-":-<25}-|-{"-":-<30}-|-{"-":-<8}-|-{"-":-<6}")
    for indice in np.where(resultado.x > 0.9)[0]:
        id_objeto = (lista_items_ordenados + lista_materiales_ordenados)[indice]

        cantidad_item = resultado.x[indice]

        if indice < len(ventas):
            # Item
            precio_objeto = ventas[id_objeto]/0.895
            nombre_objeto = item_db[id_objeto]["nombre"]
            condicion_precio = "min"

        else:
            # Material
            precio_objeto = precios_de_compra_materiales[indice - len(ventas)]
            nombre_objeto = "-"
            condicion_precio = "max"

        print(f"  {id_objeto: <25} | {nombre_objeto: <30} | {cantidad_item: <8,.0f} | {condicion_precio} {precio_objeto: <6,.0f}")

    print(f"\nPresupuesto inicial: {presupuesto:,}")
    print(f"Inversión: {cuotas_creacion + compra_materiales:,.0f}")
    print(f"  Cuotas creación: {cuotas_creacion:,.0f}")
    print(f"  Compra materiales: {compra_materiales:,.0f}")
    print(f"Ventas totales: {ventas_totales:,.0f}")
    print(f"Ganancia total: {-resultado.fun:,.0f}")