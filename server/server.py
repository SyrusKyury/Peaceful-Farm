from flask import Flask, request, g
from src.auth import requires_auth, requires_api_key
from src.config import configuration
from src.flag_submission_service import start_background_task
import src.SQlite as db
import random

app = Flask(__name__)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
@requires_auth
def public_page():
    # TODO: Mostrare informazioni sulle flag inviate e statistiche
    return "Questa è una pagina pubblica"


@app.route('/flags', methods=['POST'])
@requires_api_key
def flags():
    """
        Request body:
        {
            "api_key": "string",    # Your API key
            "flags": [              # List of flags you want to submit      
                "string", 
                ...
            ],
            "exploit": "string",    # Name of your exploit
            "service": "string",    # Service you're exploiting
            "nickname": "string"    # Your nickname
        }
    """
    # Getting the request data
    data = request.json
    
    if 'flags' not in data.keys():
        return "No flags provided", 400
    
    if 'exploit' not in data.keys():
        return "No exploit name provided", 400
    
    if 'service' not in data.keys():
        return "No service name provided", 400
    
    if 'nickname' not in data.keys():
        return "No nickname provided", 400
    
    with app.app_context():
        new_flags = db.insert_flags(data['flags'], data['service'], data['exploit'], data['nickname'])

    if new_flags == 0:
        return "I've tried to insert the provided flags, but they already exist", 200
    else:
        return "Flags inserted: " + str(new_flags), 201

# Get all the flags
@app.route('/flags', methods=['GET'])
@requires_auth
def get_flags():
    flags = db.get_flags()
    return {'flags': flags}

@app.route('/test', methods=['PUT'])
def test():
    # Getting the request data
    response_list = [
    "Accepted: X flag points",
    "Denied: invalid flag",
    "Denied: flag from nop team",
    "Denied: flag is your own",
    "Denied: flag too old",
    "Denied: flag already claimed"]

    flags = list(request.json)
    response = []
    for flag in flags:
        response.append(dict())
        response[-1]['msg'] = f'[{flag}] {random.choice(response_list)}'
        response[-1]['flag'] = flag
        response[-1]['status'] = True if response[-1]['msg'].startswith('Accepted') else False

    return response, 200

if __name__ == '__main__':
    with app.app_context():
        db.init_db()
    with app.app_context() as context:
        start_background_task(context)
    app.run(debug = True, port=configuration['peacefulFarm']['port'], use_reloader=False)
