import requests
import json
import pprint


ENDPOINT = "https://gameinfo-ams.albiononline.com/api/gameinfo/items/{}/data"

def get_item(item_id):
    response = requests.get(ENDPOINT.format(item_id))
    return response.json()

def get_crafting_requirements(item):
    return get_item(item)['craftingRequirements']['craftResourceList']


if __name__ == "__main__":
    pprint.pprint(get_crafting_requirements("T4_2H_DUALAXE_KEEPER"))