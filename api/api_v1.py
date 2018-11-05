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

app = Blueprint('api', __name__)

@app.route('/<route>')
def get_vehicles(route):
    data = {}
    # here we need to get our data from
    # DB, format it in proper way
    # and provide to future use on Front-End
    return jsonify(data)
