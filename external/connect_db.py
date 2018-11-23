from pymongo import MongoClient

def connect_db():
    client = MongoClient(port=27017)
    db = client.barrieTransit
    