# Here we'll put some code
# to run our application,
# read configs, etc.
# Any function should be placed in the other files
# and here just import
import json

from app.server import run
from db.db import DB


def check_config(data):
    # need to print some error
    # if it's not enough attrs in the config
    pass

def get_config(filename):
    with open(filename, 'r') as f:
        return json.load(f)

config = get_config('config.json')
db = DB(url=config['db']['url'])

run()
