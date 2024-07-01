from flask import Flask, request, render_template, jsonify, Response
from src.auth import requires_auth, requires_api_key
from src.config import *
import matplotlib.pyplot as plt
from flask_mysqldb import MySQL
import random
import time
from datetime import datetime, timedelta
import threading
import requests
import json
import logging
import io
import base64
import src.utils as utils

# -------------------------------------------------------------
# Flask app
# -------------------------------------------------------------

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = MYSQL_USER
app.config['MYSQL_PASSWORD'] = MYSQL_PASSWORD
app.config['MYSQL_DB'] = MYSQL_DATABASE
mysql = MySQL(app)

# -------------------------------------------------------------
# Routes
# -------------------------------------------------------------
# Index route
# -------------------------------------------------------------
@app.route('/')
@requires_auth
def index():
    return render_template('index.html', api_key=API_KEY, flag_regex=FLAG_REGEX)

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
            "flags": {
            "ip1" : ["string"],      # List of flags [flag1, flag2, flag3, ...
            "ip2" : ["string"],      # List of flags [flag1, flag2, flag3, ...
            ...
            },
            "exploit": "string",    # Name of your exploit
            "service": "string",    # Service you're exploiting
            "nickname": "string"    # Your nickname
        }
    """
    # Getting the request data
    data = request.json
    logging.info(f"Received {len(data['flags'])} flags from {data['nickname']} for {data['service']} using {data['exploit']}")
    
    if 'flags' not in data.keys() or not data['flags']:
        return "No flags provided", 400
    
    if 'exploit' not in data.keys() or not data['exploit']:
        return "No exploit name provided", 400
    
    if 'service' not in data.keys() or not data['service']:
        return "No service name provided", 400
    
    if 'nickname' not in data.keys() or not data['nickname']:
        return "No nickname provided", 400
    
    # Data sanitization
    service = data['service'].upper().replace("'", "''")
    exploit = data['exploit'].upper().replace("'", "''")
    nickname = data['nickname'].upper().replace("'", "''")
    message = None
    status = PENDING

    cursor = mysql.connection.cursor()
    new_flags = 0
    flag_dictionary = data['flags']
    for ip, flag_list in flag_dictionary.items():
        for flag in flag_list:
            try:
                cursor.execute('''INSERT INTO flags (flag, service, exploit, nickname, ip, date, status, message) 
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''',
                               (flag, service, exploit, nickname, ip, datetime.now(), status, message))
                new_flags += 1
            except:
                pass

    mysql.connection.commit()
    cursor.close()

    if new_flags == 0:
        return "I've tried to insert the provided flags, but they already exist", 400
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
    # Return the flags as a csv file
    csv = "flag,service,exploit,nickname,ip,date,status,message\n"
    for flag in flags:
        csv += f"{flag[0]},{flag[1]},{flag[2]},{flag[3]},{flag[4]},{flag[5]},{flag[6]},{flag[7]}\n"
    
    report_name = f"PF_report_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
    return Response(csv, mimetype="text/csv", headers={"Content-Disposition": f"attachment;filename={report_name}"})

# -------------------------------------------------------------
# Filter
# -------------------------------------------------------------
@app.route('/filter', methods=['GET'])
@requires_auth
def filter():
    
    # Getting the request data
    data = request.args
    if 'group' not in data.keys() or not data['group']:
        return "No group provided", 400
    
    if 't1' not in data.keys():
        return "No t1 provided", 400
    
    if 't2' not in data.keys():
        return "No t2 provided", 400
    

    t1 = data['t1'] if data['t1'] else "00:00"                  # HH:MM
    t2 = data['t2'] if data['t2'] else "23:59"                  # HH:MM
    group = data['group'].lower()                               # group by column

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
# Download client.py
# -------------------------------------------------------------
@app.route('/client', methods=['GET'])
@requires_auth
def client():
    exploit_name = utils.generate_exploit_name()
    server_ip = request.host.split(":")[0]
    server_port = request.host.split(":")[1]
    api_key = API_KEY
    n_teams = N_TEAMS
    team_id = TEAM_ID
    nop_team_id = NOP_TEAM_ID
    flag_regex = FLAG_REGEX
    submit_time = SUBMIT_TIME
    client = CLIENT_TEMPLATE % (exploit_name, server_ip, server_port, api_key, n_teams, team_id, nop_team_id, flag_regex, submit_time)

    # Return the client.py file and start the download
    return Response(client, mimetype="text/plain", headers={"Content-Disposition": "attachment;filename=client.py"})

# -------------------------------------------------------------
# Test endpoint
# -------------------------------------------------------------
@app.route('/debug', methods=['PUT'])
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
        # Choising a random response but the first one has 80% chance
        response[-1]['msg'] = random.choice(response_list[1:]) if random.random() > 0.2 else response_list[0]
        if "X" in response[-1]['msg']:
            random_float = random.uniform(5, 15)
            response[-1]['msg'] = response[-1]['msg'].replace("X",str(round(random_float, 6))) 
        response[-1]['flag'] = flag
        response[-1]['status'] = True if response[-1]['msg'].startswith('Accepted') else False

    return response, 200

# -------------------------------------------------------------
# Statistics endpoint
# -------------------------------------------------------------
@app.route('/stats', methods=['GET'])
@requires_auth
def stats():
    data = request.args
    t1 = data['t1'] if data['t1'] else "00:00"                  # HH:MM
    t2 = data['t2'] if data['t2'] else "23:59"                  # HH:MM
    type = data['type'].upper() if data['type'] else None
    value = data['value'].upper() if data['value'] else None

    if not value:
        return "No value provided", 400
    
    if not type:
        return "No type provided", 400



    t1 = datetime.now().replace(hour=int(t1.split(":")[0]), minute=int(t1.split(":")[1]))
    t2 = datetime.now().replace(hour=int(t2.split(":")[0]), minute=int(t2.split(":")[1]))

    # Divide the time between t1 and t2 in 2 minutes intervals
    # and count the number of flags for each interval (Accepted, Rejected, Pending)
    # Group by the selected type (Exploit, Service, Nickname) and filter by
    # exploit, service or nickname value

    query_template = f"""
    SELECT {type},date,status,message,flag FROM flags where date BETWEEN '{t1}' AND '{t2}' AND {type} = '{value}' ORDER BY date;"""
    cursor = mysql.connection.cursor()
    cursor.execute(query_template)
    fetch_result_list = list(cursor.fetchall())
    cursor.close()

    accepted = []
    rejected = []
    pending = []
    denied_info = {}

    while fetch_result_list:
        fetch_result = fetch_result_list.pop(0)
        start_time = fetch_result[1]
        end_time = start_time + timedelta(seconds=GAME_TICK_DURATION)
        accepted_count = 0
        rejected_count = 0
        pending_count = 0
        try:
            while fetch_result and fetch_result[1] < end_time:
                if fetch_result[2] == ACCEPTED:
                    accepted_count += 1
                elif fetch_result[2] == REJECTED:
                    denied_info[fetch_result[4]] = fetch_result[3]
                    rejected_count += 1
                elif fetch_result[2] == PENDING:
                    pending_count += 1
                if fetch_result_list:
                    fetch_result = fetch_result_list.pop(0)
                else:
                    fetch_result = None
        except Exception as e:
            return str(e), 500

        accepted.append(accepted_count)
        rejected.append(rejected_count)
        pending.append(pending_count)
    

    # Plotting a function of the number of flags for each interval
    # The x-axis represents the time intervals
    # The y-axis represents the number of flags
    # The #0D8D39 bars represent the number of accepted flags
    # The #55A5C0 bars represent the number of rejected flags

    n = len(accepted)
    x = range(n)

    # Bar width
    width = 0.35

    # Plotting
    plt.figure(figsize=(10, 5))
    plt.bar(x, accepted, width, color='#0D8D39', label='Accepted')
    plt.bar([i + width for i in x], rejected, width, color='#55A5C0', label='Rejected')

    # Setting the x-axis labels
    plt.xlabel('Ticks')
    plt.ylabel('Number of flags')
    plt.title(f"Flags statistics for {type} {value} from {t1.strftime('%H:%M')} to {t2.strftime('%H:%M')}")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Saving the plot to a buffer
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    render_title = f"Flags statistics for {type} {value} from {t1.strftime('%H:%M')} to {t2.strftime('%H:%M')}"
    return render_template('stats.html', image=base64.b64encode(img.read()).decode('utf-8'), denied_info=denied_info, render_title=render_title)

# -----------------------------------------------------------------------------------
# Background task
# -----------------------------------------------------------------------------------
def timestamp():
    return datetime.now().time().replace(microsecond=0)

# -----------------------------------------------------------------------------------
# Background task
# -----------------------------------------------------------------------------------

def background_task():
    game_start = datetime.now().replace(hour=COMPETITION_START_TIME[0], minute=COMPETITION_START_TIME[1], second=COMPETITION_START_TIME[2], microsecond=0)
    seconds_since_gamestart: float = (datetime.now() - game_start).total_seconds()
    current_round: int = 1 + seconds_since_gamestart // GAME_TICK_DURATION

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
        next_round_seconds_offset = GAME_TICK_DURATION * current_round
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
        try:
            submit_flags()
        except Exception as e:
            logging.error(f"\t\tError submitting flags: {e}")

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
        
        if FLAGS_SUBMISSION_DEBUG:
            url = f"http://localhost:{PEACEFUL_FARM_SERVER_PORT}/debug"
        else:
            url = "http://{ip}:{port}{api_endpoint}".format(ip=SUBMISSION_SERVER_IP, port=SUBMISSION_SERVER_PORT, api_endpoint=SUBMISSION_SERVER_API_ENDPOINT)
        
        accepted_flags = 0
        result = requests.put(url, headers={'X-Team-Token': SUBMISSION_SERVER_TEAM_TOKEN}, json=flags).text
        result = json.loads(result)
        if result == {'code': 'GAME_ENDED', 'message': '[GAME_ENDED] Game ended'}:
            logging.info("\t\tGame has ended")
            return
        
        for res in result:
            if 'Accepted' in res['msg']:
                status = ACCEPTED
                accepted_flags += 1
            else:
                status = REJECTED
            cur.execute('''UPDATE flags SET status = %s, message = %s WHERE flag = %s AND status = %s''', (status, res['msg'], res['flag'], str(PENDING)))

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
    print("Starting the Peaceful Farm server...")
    print("Starting time: ", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print(settings_feedback)

    print("Starting the web server...")
    print("Connecting to the database...")
    with app.app_context():
        while True:
            try:
                mysql.connection.ping()
                print("Connection established")
                break
            except Exception as e:
                time.sleep(1)

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
    thread.daemon = True
    thread.start()
    
    app.run(debug=FLASK_DEBUG, host="0.0.0.0", port=PEACEFUL_FARM_SERVER_PORT)