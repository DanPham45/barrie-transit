from pymongo import MongoClient

def get_db():
    client = MongoClient(port=27017)
    db = client.barrieTransit
    return db
    