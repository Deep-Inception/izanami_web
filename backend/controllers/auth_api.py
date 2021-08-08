from backend import app
from flask import request
from werkzeug.exceptions import Unauthorized

def api_auth():
    token = request.args.get('token')
    key = app.config["API_AUTH_KEY"]
    if key != token:
        raise Unauthorized
