"""
This module contains out base APIs
that should be used on Front-End side.

Here we put only simple functions that
use DB/any_other related functions
from different modules.
"""
from flask import (
    Blueprint,
    jsonify,
)

from app.utils import get_db

__version__ = 'v1.0'
app = Blueprint('api', __name__)

@app.route('/get_all_routes')
def get_route_names():
    """
    Returns all possible route names
    for routes that have tracked.
    
    Get something like this
    {"routes": ["100A", "8A"]}
    """
    db = get_db()
    cursor = db.get_all_routes_name()
    routes = [route for route in cursor]
    return jsonify({'routes': routes})

@app.route('/get_bus_num')
def get_bus_num():
    """
    Returns number of buses that have tracked.
    
    Get {'NumOfVehicle': 21}
    from DB but returns
    {'num_of_routes': <NUMBER>}
    to follow same name convention
    """
    db = get_db()
    result = db.get_number_of_buses()
    return jsonify({
        'num_of_vehicles': result.get('NumOfVehicle'),
    })

@app.route('/get_routes_num')
def get_routes_num():
    """
    Returns number of routes that have tracked.

    Get {'NumOfRoute': <NUMBER>}
    from DB but returns
    {'num_of_routes': <NUMBER>}
    to follow same name convention
    """
    db = get_db()
    number = db.get_number_of_routes()
    return jsonify({'num_of_routes': number.get('NumOfRoute')})

@app.route('/get_track_days')
def get_track_days():
    """
    Returns number difference
    betwwen first and last record date
    in DB.

    Returs {'days': <NUMBER>}
    """
    db = get_db()
    return jsonify({'days': db.get_days_of_tracking()})

@app.route('/get_avg_pass')
def get_avg_pass():
    """
    Returns average number of passenagers per route.

    Returns {
        'results': [
            [
                <ROUTE_NAME>,
                <NUMBER>
            ],
            ...
        ]
    }
    """
    db = get_db()
    return jsonify({'results': db.get_avg_per_route()})

@app.route('/get_avg_route_stop')
def get_avg_pass_route_stop():
    """
    TODO:
    """
    db = get_db()
    return jsonify({'results': list(db.get_avg_route_stop())})

@app.route('/get_compare_routes')
def get_compare_routes():
    """
    TODO:
    """
    db = get_db()
    return jsonify({'results': list(db.compare_routes())})


@app.route('/get_avg_per_stop_location')
def get_avg_per_stop_location():
    """
    TODO:
    """
    db = get_db()
    return jsonify(db.avg_per_stop_location())