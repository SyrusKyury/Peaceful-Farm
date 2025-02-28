# --------------------------------------------------------------------------------------------------------------------------
# Desc: This file is responsible for both the basic authentication for the web interface and the API key authentication for
# the client. The basic authentication is used to protect the web interface from unauthorized access. The API key
# authentication is used to protect the server from unauthorized clients. The API key is stored in the configuration file.
# - An API Route is protected using the requires_api_key decorator
# - A Web Route is protected using the requires_auth decorator
#
# Version: 1.0
# Author: Raffaele D'Ambrosio
# Full Path: server/web/app/src/utils/auth.py
# Creation Date: 09/07/2024
# --------------------------------------------------------------------------------------------------------------------------

from flask import request, render_template, session, redirect
from settings import *
import hashlib

def check_credentials(username, password):
    for account in SETTINGS['ACCOUNTS']['value']:
        if account['username'] == username and account['password'] == password:
            return True
    return False


def check_hash(hash):
    for account in SETTINGS['ACCOUNTS']['value']:
        if hash == generate_hash(account['username'], account['password']):
            return True
    return False


def generate_hash(username, password):
    return hashlib.sha256(f"{username}:{password}".encode()).hexdigest()


def requires_auth(f):
    def decorated(*args, **kwargs):
        # Check if authentification is required
        if not SETTINGS['REQUIRE_AUTHENTICATION']['value']:
            return f(*args, **kwargs)
        
        # Check if the user has a valid session
        auth = session.get('auth')
        if not auth or not check_hash(auth):
            return redirect('/login')
    
        return f(*args, **kwargs)
    decorated.__name__ = f.__name__  # Questo è necessario per evitare problemi con Flask
    return decorated


def requires_api_key(f):
    def decorated(*args, **kwargs):
        # Check if authentification is required
        if 'api_key' not in request.json.keys() or request.json['api_key'] != SETTINGS['API_KEY']['value']:
            return "Unauthorized client", 401
        return f(*args, **kwargs)
    
    decorated.__name__ = f.__name__  # Questo è necessario per evitare problemi con Flask
    return decorated
