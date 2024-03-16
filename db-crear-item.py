import json

with open("item-db.json","r") as file:
    item_db = json.load(file)

first_time = True
item_id = None
item_db_keys = list(item_db.keys())

while (item_id in item_db_keys) or first_time:
    item_id = input("ID: ")
    first_time = False

item_name = input("Nombre completo: ")
item_type = input("Tipo de objeto: ")
item_value = int(input("Valor de objeto: "))
item_tier = int(input("Nivel: "))
item_enchantment = int(input("Encantamiento: "))
item_station = input("Estación crafting: ")
item_planks = int(input("Tablas: "))
item_metalbars = int(input("Lingotes: "))
item_cloth = int(input("Tela: "))
item_leather = int(input("Cuero: "))

new_item = {
    "id": item_id,
    "nombre": item_name,
    "tipo": item_type,
    "valor": item_value,
    "nivel": item_tier,
    "encantamiento": item_enchantment,
    "estacion": item_station,
    "tablas": item_planks,
    "lingotes": item_metalbars,
    "tela": item_cloth,
    "cuero": item_leather
}

item_db[item_id] = new_item

with open("item-db.json","w") as file:
    json.dump(item_db, file)

print("\nItem saved successfully\n")