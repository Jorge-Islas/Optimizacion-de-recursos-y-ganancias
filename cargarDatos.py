import json

def cargar_item_db():
    with open("item-db.json", "r") as file:
        item_db = json.load(file)
    return item_db