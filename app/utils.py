import os
from db.db import DB

db = None

def get_db():
    global db
    if db is None:
        db = DB(url=os.environ.get('bus_dburl', 'mongodb://barrieTransit:BarrieTransit@ec2-18-222-217-102.us-east-2.compute.amazonaws.com:27017')) 
    return db
