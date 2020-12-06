import os
from pymongo import MongoClient
from config.config_json import get_config

def connection():
    client = MongoClient(os.environ.get("MONGODB_URL") or get_config()["mongoAtlas"])
    db  = client.cfpm
    return db
