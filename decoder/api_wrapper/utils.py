import json
from json import encoder
import requests
import os


session = requests.Session()

def read_json_file(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_card_set_online(expansion: str, region="en_us"):
    url = f'http://dd.b.pvp.net/latest/{expansion}/{region}/data/{expansion}-{region}.json'
    print('Loading: ', url) 
    r = session.get(url)
    r.encoding = 'utf8'
    return r.json()


def get_lor_globals(region="en_us"):
    url = f"https://dd.b.pvp.net/latest/core/{region}/data/globals-{region}.json"
    print('Loading: ', url)
    r = session.get(url)
    return r.json()

def write_json_file(json_data,json_path):
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
