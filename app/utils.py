import os
from db.db import DB

db = None

def get_db():
    global db
    if db is None:
        db = DB(url=os.environ.get('bus_dburl', 'localhost:27017'))
    return db
