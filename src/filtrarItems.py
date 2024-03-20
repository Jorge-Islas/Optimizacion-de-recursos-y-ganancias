import pandas as pd

def agregar_tipos_de_item(registro_de_items):
    agregar_categorías=[]
    categoria = ""

    while True:
        categoria = input("Agregar categoría ('n' para continuar): ")
        if categoria == "n":
            break
        agregar_categorías.append(categoria)

    if len(agregar_categorías) > 0:
        registro_de_items = registro_de_items[registro_de_items["tipo"].isin(agregar_categorías)]

    print()
    return registro_de_items

def quitar_tipos_de_item(registro_de_items):
    quitar_categorías=[]
    categoria = ""

    while True:
        categoria = input("Quitar categoría ('n' para continuar): ")
        if categoria == "n":
            break
        quitar_categorías.append(categoria)

    filtro = ~registro_de_items["tipo"].isin(quitar_categorías)
    registro_de_items = registro_de_items[filtro]

    return registro_de_items

def filtrar_items(registro_de_items):
    
    registro_de_items = agregar_tipos_de_item(registro_de_items)
    registro_de_items = quitar_tipos_de_item(registro_de_items)

    print(registro_de_items)
    print()
    return registro_de_items