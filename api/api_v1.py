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
    """
        Returns something like this
        {"routes": ["100A", "8A"]}
    """
    # TODO: use config
    db = DB('localhost:27017')

    cursor = db.get_all_routes_name()
    routes = [route for route in cursor]
    return jsonify({'routes': routes})

@app.route('/get_bus_num')
def get_bus_num():
    # Returs {'NumOfVehicle': 21}
    db = DB('localhost:27017')
    number = db.get_number_of_buses()
    return jsonify(number)

@app.route('/get_routes_num')
def get_routes_num():
    # Returs {'NumOfRoute': 24}
    db = DB('localhost:27017')
    number = db.get_number_of_routes()
    return jsonify(number)

@app.route('/get_track_days')
def get_track_days():
    # Returs just number (days)
    db = DB('localhost:27017')
    number = db.get_days_of_tracking()
    return jsonify({'days': number})
