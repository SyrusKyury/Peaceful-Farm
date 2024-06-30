from flask import request, render_template
from src.config import *

def check_auth(username, password):
    for account in ACCOUNTS:
        if account['username'] == username and account['password'] == password:
            return True
    return False

def authenticate():
    return render_template('403.html'), 401, {'WWW-Authenticate': 'Basic realm="Login Required"'}


def requires_auth(f):
    def decorated(*args, **kwargs):
        # Check if authentification is required
        if not REQUIRE_AUTHENTICATION:
            return f(*args, **kwargs)
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    decorated.__name__ = f.__name__  # Questo è necessario per evitare problemi con Flask
    return decorated

def requires_api_key(f):
    def decorated(*args, **kwargs):
        # Check if authentification is required
        if 'api_key' not in request.json.keys() or request.json['api_key'] != API_KEY:
            return "Unauthorized client", 401
        return f(*args, **kwargs)
    
    decorated.__name__ = f.__name__  # Questo è necessario per evitare problemi con Flask
    return decorated
