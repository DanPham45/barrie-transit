"""
This module contains out base APIs
that should be used on Front-End side.

Here we put only simple functions that
use DB/any_other related functions from different modules.

Moreover, we'll use https://flask-apispec.readthedocs.io/en/latest/usage.html
to make out APIs much more professional 
"""
from flask import (
    Blueprint,
    jsonify,
)

from db.db import DB

__version__ = 'v1.0'
app = Blueprint('api', __name__)

@app.route('/get_routes')
def get_routes():
    data = {'routes': [{'name': '100D', 'key': '123'}]}
    # data = get_routes_from_db()
    return jsonify(data)

@app.route('/<route>')
def get_vehicles(route):
    data = {}
    # here we need to get our data from
    # DB, format it in proper way
    # and provide to future use on Front-End
    #1 routes: front end come to get data
    #2 GET: url, limited data # post: more data
    return jsonify(data)

@app.route('/get_all_routes')
def get_route_names():
	# {"routes": ["100A", "8A"]}

    # TODO: use config
    db = DB('localhost:27017')
    return jsonify(db.get_all_routes_name())
