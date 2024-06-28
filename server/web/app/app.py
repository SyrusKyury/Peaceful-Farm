from flask import Flask, request, g, render_template, jsonify
from src.auth import requires_auth, requires_api_key
from src.config import banner, configuration
from flask_mysqldb import MySQL
import random
import time
from datetime import datetime, timedelta
import threading
import requests
import json
import logging

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'napoli'
app.config['MYSQL_PASSWORD'] = 'forza_napoli'
app.config['MYSQL_DB'] = 'cyber_challenge'
mysql = MySQL(app)

# ----------------- Constants -----------------

PENDING = 0
ACCEPTED = 1
REJECTED = 2

# ---------------------------------------------


@app.route('/')
@requires_auth
def public_page():
    return render_template('index.html')

# -------------------------------------------------------------
# Api to submit flags to the database
# -------------------------------------------------------------

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
    print(f"Received {len(data['flags'])} flags from {data['nickname']} for {data['service']} using {data['exploit']}")
    
    if 'flags' not in data.keys() or not data['flags']:
        return "No flags provided", 400
    
    if 'exploit' not in data.keys() or not data['exploit']:
        return "No exploit name provided", 400
    
    if 'service' not in data.keys() or not data['service']:
        return "No service name provided", 400
    
    if 'nickname' not in data.keys() or not data['nickname']:
        return "No nickname provided", 400
    
    service = data['service'].upper()
    exploit = data['exploit'].upper()
    nickname = data['nickname'].upper()
    message = None
    status = PENDING

    cursor = mysql.connection.cursor()
    new_flags = 0
    for flag in data['flags']:
        try:
            cursor.execute('''INSERT INTO flags (flag, service, exploit, nickname, date, status, message) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                           (flag, service, exploit, nickname, datetime.now(), status, message))
            new_flags += 1
        except:
            pass

    mysql.connection.commit()
    cursor.close()

    if new_flags == 0:
        return "I've tried to insert the provided flags, but they already exist", 200
    else:
        return "Flags inserted: " + str(new_flags), 201

# -------------------------------------------------------------
# Get all flags
# -------------------------------------------------------------

@app.route('/flags', methods=['GET'])
@requires_auth
def get_flags():
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM flags''')
    flags = cursor.fetchall()
    cursor.close()
    return {'flags': flags}

# -------------------------------------------------------------
# Filter
# -------------------------------------------------------------

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

    t1 = datetime.now().replace(hour=int(t1.split(":")[0]), minute=int(t1.split(":")[1]))
    t2 = datetime.now().replace(hour=int(t2.split(":")[0]), minute=int(t2.split(":")[1]))
    
    query = f"""
    SELECT 
        {group} AS selected_group,
        SUM(CASE WHEN status = 1 THEN 1 ELSE 0 END) AS Accepted,
        SUM(CASE WHEN status = 2 THEN 1 ELSE 0 END) AS Rejected,
        SUM(CASE WHEN status = 0 THEN 1 ELSE 0 END) AS Pending
        FROM flags
        WHERE date BETWEEN '{t1}' AND '{t2}'
        GROUP BY selected_group;
    """

    cursor = mysql.connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return jsonify(result), 200

# -------------------------------------------------------------
# Test endpoint
# -------------------------------------------------------------

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

# -----------------------------------------------------------------------------------
# Background task
# -----------------------------------------------------------------------------------

def timestamp():
    return datetime.now().time().replace(microsecond=0)

# -----------------------------------------------------------------------------------
# Background task
# -----------------------------------------------------------------------------------

GAMETICK_DURATION = configuration["flagServer"]["game_tick_duration"]
FLAGS_SUBMISSION_WINDOW = configuration["flagServer"]["flags_submission_window"]

def background_task():
    game_start = datetime.now().replace(hour=11, minute=0, second=0, microsecond=0)
    seconds_since_gamestart: float = (datetime.now() - game_start).total_seconds()
    current_round: int = 1 + seconds_since_gamestart // GAMETICK_DURATION

    logging.info("\t\t" + "-"*50)
    logging.info("\t\tGame information")
    logging.info("\t\t" + "-"*50)
    logging.info(f"\t\tGame started at {game_start}")
    logging.info(f"\t\tCurrent round: {current_round}")
    logging.info("\t\t" + "-"*50 + "\n\n\n\n")
    submit_flags()

    if current_round < 0:
        logging.info("\t\tGame has not started yet")
        logging.info(f"\t\tGame will start in {game_start - datetime.now()}")
        time.sleep((game_start - datetime.now()).total_seconds())
        logging.info("\t\tGame started")

    while True:
        next_round_seconds_offset = GAMETICK_DURATION * current_round
        minutes, seconds = divmod(next_round_seconds_offset, 60)
        hours, minutes = divmod(minutes, 60)
        next_round_diff: float = timedelta(
            hours=hours, minutes=minutes, seconds=seconds
        )
        seconds_until_next_round = (
            game_start + next_round_diff - datetime.now()
        ).total_seconds()

        to_wait = seconds_until_next_round - FLAGS_SUBMISSION_WINDOW

        if to_wait < 0:
            to_wait = 0

        logging.info(
            f"\t\t[{timestamp()}] Waiting {to_wait:.2f} seconds before submitting"
        )
        time.sleep(to_wait)
        submit_flags()

        time.sleep(FLAGS_SUBMISSION_WINDOW + 5)
        current_round += 1

# -----------------------------------------------------------------------------------
# Submit flags function
# -----------------------------------------------------------------------------------

def submit_flags():
    with app.app_context():
        cur = mysql.connection.cursor()
        # Get all pending flags
        cur.execute('''SELECT * FROM flags WHERE status = %s''', (str(PENDING)))
        flags = cur.fetchall()
        flags = [i[0] for i in flags]

        if len(flags) == 0:
            logging.info("\t\tNo flags to submit")
            return
        
        if len(flags) == 1:
            logging.info(f"\t\tI'm submitting 1 flag...")
        else:
            logging.info(f"\t\tI'm submitting {len(flags)} flags...")
        
        accepted_flags = 0
        url = "http://{ip}:{port}{api_endpoint}".format(ip=configuration["flagServer"]["ip"], port=configuration["flagServer"]["port"], api_endpoint=configuration["flagServer"]["api_endpoint"])
        result = requests.put(url, headers={'X-Team-Token': configuration["flagServer"]["team_token"]}, json=flags).text
        result = json.loads(result)
        for res in result:
            if 'Accepted' in res['msg']:
                status = ACCEPTED
                accepted_flags += 1
            else:
                status = REJECTED
            cur.execute('''UPDATE flags SET status = %s, message = %s WHERE flag = %s''', (status, res['msg'], res['flag']))

        mysql.connection.commit()
        cur.close()

        logging.info("\t\t" + "-"*50)
        logging.info(f"\t\tSubmitted flags: {len(flags)}")
        logging.info(f"\t\tAccepted flags: {accepted_flags}")
        logging.info(f"\t\tRejected flags: {len(flags) - accepted_flags}")
        logging.info("\t\t" + "-"*50)


# -------------------------------------------------------------
# Main
# -------------------------------------------------------------

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(banner)

    # Initialize the database with the schema
    with app.app_context():
        cur = mysql.connection.cursor()
        with open('src/schema.sql', 'r') as f:
            schema_sql = f.read()
        try:
            cur.execute(schema_sql)
        except:
            pass
        finally:
            mysql.connection.commit()
            cur.close()

    # Start the background task in a separate thread but with higher priority
    thread = threading.Thread(target=background_task)
    thread = threading.Thread(target=background_task)
    thread.daemon = True
    thread.start()
    
    app.run(debug=True, host="0.0.0.0")