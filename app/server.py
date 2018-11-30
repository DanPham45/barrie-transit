import os
from os.path import (
    abspath,
    join,
)
from flask import (
    Flask,
    render_template,
)
from api.api_v1 import app as api_v1 

__version__ = 'v1.0'
template_dir = abspath(join('..', 'templates'))
static_dir = abspath(join('..', 'static'))

app = Flask(__name__)
app.register_blueprint(api_v1, url_prefix='/api_v1')

@app.route('/')
def index():
    content = 'some very first initial data? Anywa, it\'s a hello world example'
    return render_template('index.html', content=content)

def run():
    # debug=True/False shoud be taken from config.json
    # and definitely turn off for final release!
    host = os.environ.get('bus_host')
    port = os.environ.get('bus_port')
    debug = os.environ.get('bus_debug', False)
    if host and port:
        app.run(debug=debug, host=host, port=port)
    else:
        app.run(debug=debug)
