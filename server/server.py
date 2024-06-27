from flask import Flask, request, g, render_template
from src.auth import requires_auth, requires_api_key
from src.config import configuration, banner
from src.flag_submission_service import start_background_task
import datetime
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
    return render_template('index.html')


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
    
    if 'flags' not in data.keys() or not data['flags']:
        return "No flags provided", 400
    
    if 'exploit' not in data.keys() or not data['exploit']:
        return "No exploit name provided", 400
    
    if 'service' not in data.keys() or not data['service']:
        return "No service name provided", 400
    
    if 'nickname' not in data.keys() or not data['nickname']:
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

@app.route('/filter', methods=['GET'])
@requires_auth
def filter():
    
    # Getting the request data
    data = request.args
    if 'group' not in data.keys():
        return "No group provided", 400
    
    if 't1' not in data.keys():
        return "No t1 provided", 400
    
    if 't2' not in data.keys():
        return "No t2 provided", 400
    

    t1 = data['t1']                 # HH:MM
    t2 = data['t2']                 # HH:MM
    group = data['group'].lower()   # group by column

    t1 = datetime.datetime.now().replace(hour=int(t1.split(":")[0]), minute=int(t1.split(":")[1]))
    t2 = datetime.datetime.now().replace(hour=int(t2.split(":")[0]), minute=int(t2.split(":")[1]))
    
    return db.get_flags_statistics(group, t1, t2)


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
    print(banner)
    with app.app_context():
        db.init_db()
    with app.app_context() as context:
        start_background_task(context)
    app.run(debug = False, port=configuration['peacefulFarm']['port'])
