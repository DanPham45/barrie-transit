import binascii
import os
from os.path import (
    abspath,
    join,
)

from flask import (
    Flask,
    flash,
    render_template,
    redirect,
    request,
    url_for,
    session,
    g,
)

from api.api_v1 import app as api_v1
from app.utils import get_db

__version__ = 'v1.0'

app = Flask(__name__)
app.register_blueprint(api_v1, url_prefix='/api_v1')
db = get_db()

@app.route('/')
def index():
    # email = session.get('email')
    # if not email:
    #     return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form.get('email')
    password = request.form.get('password')

    if email is None or password is None:
        return render_template('login.html')

    if db.has_access(email=email, raw_password=password):
        session['email'] = email
    else:
        flash('The email address or password is incorrect')
        return render_template('login.html')

    return redirect(url_for('index'))

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))

def run():
    host = os.environ.get('bus_host')
    port = os.environ.get('bus_port')
    debug = os.environ.get('bus_debug', True)
    app.secret_key = os.environ.get(
        'bus_secret',
        binascii.hexlify(os.urandom(24)).decode(),
    )
    if host and port:
        app.run(debug=debug, host=host, port=int(port))
    else:
        app.run(debug=debug)

if __name__ == "__main__":
    run()
