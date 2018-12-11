from app.server import app
import os
import binascii

host = os.environ.get('bus_host')
port = os.environ.get('bus_port')
debug = os.environ.get('bus_debug', True)
app.secret_key = os.environ.get(
    'bus_secret',
    binascii.hexlify(os.urandom(24)).decode(),
)