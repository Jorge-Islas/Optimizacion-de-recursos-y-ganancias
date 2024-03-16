import json
import pandas as pd

with open("item-db.json", "r") as file:
    item_db = json.load(file)

df = pd.DataFrame(list(item_db.values()))

df.to_csv("item-db-csv.csv")