import json
from pymongo import MongoClient

def get_db_url():
    with open("config/config.json", encoding="utf-8") as config_file:
        return json.load(config_file) or None

def connection():
    client = MongoClient(get_db_url()["mongoAtlas"])
    db  = client.cfpm
    return db
