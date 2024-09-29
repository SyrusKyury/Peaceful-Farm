from flask import render_template, request, Response, jsonify
from src.utils.auth import requires_auth, requires_api_key
from settings import *
from src.utils import utils
from src.flag import Flag
from src.database import insert_pending_flags, get_all_flags, filter_query, stats_query
from datetime import datetime
from src.base import app
import importlib
import threading
import logging

protocol_module = importlib.import_module("plugins." + SUBMISSION_PROTOCOL)

# -------------------------------------------------------------
# Routes
# -------------------------------------------------------------
# Index route
# -------------------------------------------------------------
@app.route('/')
@requires_auth
def index():
    return render_template('index.html', api_key=API_KEY, flag_regex=protocol_module.FLAG_REGEX)

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
    logging.info(f"Received {sum(len(flags) for flags in data['flags'].values())} flags from {data['nickname']} for {data['service']} using {data['exploit']}")

    if 'flags' not in data.keys() or not data['flags']:
        return "No flags provided", 400
    
    if 'exploit' not in data.keys() or not data['exploit']:
        return "No exploit name provided", 400
    
    if 'service' not in data.keys() or not data['service']:
        return "No service name provided", 400
    
    if 'nickname' not in data.keys() or not data['nickname']:
        return "No nickname provided", 400
    
    # Data
    service = data['service'].upper()
    exploit = data['exploit'].upper()
    nickname = data['nickname'].upper()
    date = datetime.now()

    #TODO: Improve in order to call insert_pending_flags only once
    for ip, request_flag_list in data['flags'].items():
        ip_flag_list = [Flag(flag=flag_i, service=service, exploit=exploit, nickname=nickname, ip=ip, date=date) for flag_i in request_flag_list]
        insert_pending_flags(ip_flag_list)

    return f"Received {sum(len(flags) for flags in data['flags'].values())} flags from {data['nickname']} for {data['service']} using {data['exploit']}", 200

# -------------------------------------------------------------
# Get all flags
# -------------------------------------------------------------
@app.route('/flags', methods=['GET'])
@requires_auth
def get_flags():
    flags = get_all_flags()

    # Return the flags as a csv file
    csv = "flag,service,exploit,nickname,ip,date,status,message\n"
    for flag in flags:
        csv += f"{flag.flag},{flag.service},{flag.exploit},{flag.nickname},{flag.ip},{flag.date},{flag.status},{flag.message}\n"

    report_name = f"PF_report_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
    return Response(csv, mimetype="text/csv", headers={"Content-Disposition": f"attachment;filename={report_name}"})

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
    submit_time = SUBMIT_TIME
    attack_time = ATTACK_TIME
    client = CLIENT_TEMPLATE % (exploit_name, server_ip, server_port, api_key, submit_time, protocol_module.FLAG_REGEX, attack_time)

    # Return the client.py file and start the download
    return Response(client, mimetype="text/plain", headers={"Content-Disposition": "attachment;filename=client.py"})


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

    return jsonify(filter_query(group, t1, t2)), 200

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

    flags = stats_query(t1, t2, type, value)
    if not flags:
        return render_template('stats.html', image=b"", denied_info={}, render_title="No flags found")

    t1_int = utils.datetime_to_int(t1)
    t2_int = utils.datetime_to_int(t2)

    time_slots = range(t1_int, t2_int, GAME_TICK_DURATION)
    start_slot = time_slots[0]
    accepted = []
    rejected = []
    denied_info = {}

    for i in time_slots[1:]:
        accepted_count = 0
        rejected_count = 0

        while flags and utils.datetime_to_int(flags[0].date) < i and utils.datetime_to_int(flags[0].date) > start_slot:
            flag = flags.pop(0)
            if flag.status == ACCEPTED:
                accepted_count += 1
            else:
                rejected_count += 1
                denied_info[flag.flag] = flag.message

        start_slot = i
        accepted.append(accepted_count)
        rejected.append(rejected_count)

    while accepted[0] == 0 and rejected[0] == 0:
        accepted.pop(0)
        rejected.pop(0)
    
    while accepted[-1] == 0 and rejected[-1] == 0:
        accepted.pop(-1)
        rejected.pop(-1)

    img = utils.plot_flag_statistics(accepted, rejected, type, value, t1, t2)
    render_title = f"Flags statistics for {type} {value} from {t1.strftime('%H:%M')} to {t2.strftime('%H:%M')}"
    return render_template('stats.html', image=img, denied_info=denied_info, render_title=render_title)

# -------------------------------------------------------------
# Main
# -------------------------------------------------------------

from src.submission_service import timed_submission

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(banner)
    print("Starting the Peaceful Farm server...")
    print("Starting time: ", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print(settings_feedback)

    # Start the background task in a separate thread
    print("Starting the background task...")
    thread = threading.Thread(target=timed_submission)
    thread.daemon = True
    thread.start()
    
    app.run(debug=FLASK_DEBUG, host="0.0.0.0", port=PEACEFUL_FARM_SERVER_PORT)