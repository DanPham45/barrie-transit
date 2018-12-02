import os
from os.path import (
    abspath,
    join,
)
from flask import (
    Flask,
    render_template,
    g,
)
from api.api_v1 import app as api_v1

__version__ = 'v1.0'

app = Flask(__name__)
app.register_blueprint(api_v1, url_prefix='/api_v1')

@app.route('/')
def index():
    return render_template('index.html')

def run():
    host = os.environ.get('bus_host')
    port = os.environ.get('bus_port')
    debug = os.environ.get('bus_debug', True)
    if host and port:
        app.run(debug=debug, host=host, port=int(port))
    else:
        app.run(debug=debug)
