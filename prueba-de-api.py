import requests
import json
from datetime import datetime, timedelta

# API endpoint for Albion Online Data Project
ALBION_DATA_URL = "https://west.albion-online-data.com/api/v2/stats/prices/"

item_list = ["T3_MAIN_DAGGER", "T4_MAIN_DAGGER", "T4_MAIN_RAPIER_MORGANA", "T4_MAIN_RAPIER_MORGANA@1"]

location = "FortSterling"

# normal, bueno, notable, sobresaliente, obra maestra, todas
#   1       2       3           4             5          0
qualities = [1,2,3]

def format_URL(item_list, location, qualities):
    return ALBION_DATA_URL + ",".join(item_list) + ".json?locations="+location+"&qualities=" + ",".join([str(quality) for quality in qualities])

def save_response_to_json(response, file_name="tmp.json"):
    with open(file_name, "w") as file:
        json.dump(response, file)

request_URL = format_URL(item_list, location, qualities)

response = requests.get(request_URL)

save_response_to_json(response.json())