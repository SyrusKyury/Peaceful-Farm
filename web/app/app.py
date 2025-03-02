from flask import render_template, request, Response, jsonify, session, redirect
from settings import *
import src.utils.utils as utils
from src.flag import Flag
from datetime import datetime
from src.base import app, notification_service, submission_service, database_service, auth_service, plugin
import logging
import copy


# -------------------------------------------------------------
# Routes
# -------------------------------------------------------------
# Index route
# -------------------------------------------------------------
@app.route('/')
@auth_service.requires_auth
def index():
    return render_template('index.html',
                           address = request.host,
                           start = SETTINGS['COMPETITION_START_TIME']['value'].isoformat(),
                           tick = SETTINGS['GAME_TICK_DURATION']['value']*1000,
                           api_key = SETTINGS['API_KEY']['value'])


# -------------------------------------------------------------
# Login route
# -------------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print("Form:", request.form)
        username, password = request.form['username'], request.form['password']
        if auth_service.check_credentials(username, password):
            session['auth'] = auth_service.generate_hash(username, password)
            if SETTINGS['OPEN_OPTIONS_ON_LOGIN']['value']:
                return redirect('settings')
            else:
                return redirect('/')
    else:
        username, password = request.args.get('username'), request.args.get('password')
        if session.get('auth') and auth_service.check_hash(session.get('auth')):
            return redirect('/')
        else:
            session.clear()
            return render_template('login.html')
        

# -------------------------------------------------------------
# Logout route
# -------------------------------------------------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')    


# -------------------------------------------------------------
# Api to submit flags to the database
# -------------------------------------------------------------
@app.route('/flags', methods=['POST'])
@auth_service.requires_api_key
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
            "nickname": "string",   # Your nickname
            "urgent": bool          # Signal to send the flags immediately
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
    urgent = data.get('urgent')

    #TODO: Improve in order to call insert_pending_flags only once
    for ip, request_flag_list in data['flags'].items():
        ip_flag_list = [Flag(flag=flag_i, service=service, exploit=exploit, nickname=nickname, ip=ip, date=date) for flag_i in request_flag_list]
        database_service.insert_pending_flags(ip_flag_list)

    msg = f"""
    <strong>Received flags:</strong> {sum(len(flags) for flags in data['flags'].values())}<br>
    <strong>Attacker:</strong> {data['nickname']}<br>
    <strong>Service:</strong> {data['service']}<br>
    <strong>Exploit:</strong> {data['exploit']}
    """
    notification_service.send_notification(msg)
    if urgent:
        submission_service.urgent()
    
    return f"Received {sum(len(flags) for flags in data['flags'].values())} flags from {data['nickname']} for {data['service']} using {data['exploit']}", 200

# -------------------------------------------------------------
# Get all flags
# -------------------------------------------------------------
@app.route('/csv', methods=['GET'])
@auth_service.requires_auth
def get_flags():
    flags = database_service.get_all_flags()

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
@auth_service.requires_auth
def client():
    exploit_name = utils.generate_exploit_name()
    server_ip = request.host.split(":")[0]
    server_port = request.host.split(":")[1]
    api_key = SETTINGS['API_KEY']['value']
    submit_time = SETTINGS['SUBMIT_TIME']['value']
    attack_time = SETTINGS['ATTACK_TIME']['value']
    client = CLIENT_TEMPLATE % (exploit_name, server_ip, server_port, api_key, submit_time, plugin.settings['FLAG_REGEX']['value'], attack_time)

    # Return the client.py file and start the download
    return Response(client, mimetype="text/plain", headers={"Content-Disposition": "attachment;filename=client.py"})


# -------------------------------------------------------------
# Settings
# -------------------------------------------------------------
@app.route('/settings', methods=['GET', 'POST'])
@auth_service.requires_auth
def settings():
    global SETTINGS
    
    if request.method == 'POST':

        settings_file = copy.deepcopy(SETTINGS)
        protocol_settings_file = copy.deepcopy(plugin.settings)
        #raise Exception(request.json.items())

        for key, value in request.json.items():
            option_name = key.split('[')[1:]
            option_name = ''.join(option_name)[:-1]
            

            # Try to handle JSON values
            try:
                parsed_value = json.loads(value.replace('\'', '"'))
            except json.JSONDecodeError:
                parsed_value = value

            # If it's a string, check for boolean representations
            if value.lower() == 'true':
                value_to_store = True
            elif value.lower() == 'false':
                value_to_store = False
            else:
                value_to_store = parsed_value

            if 'plugin_settings' in key:
                protocol_settings_file[option_name]['value'] = value_to_store
            else:
                settings_file[option_name]['value'] = value_to_store
            
        with open('settings.json', 'w') as s:
            json.dump(settings_file, s, indent=4)
        
        with open(plugin.settings_path, 'w') as s:
            json.dump(protocol_settings_file, s, indent=4)

        submission_service.stop()
        SETTINGS = init_settings()
        plugin.settings = plugin.init_settings()
        submission_service.start()

        return redirect('/settings')
    else:
        return render_template('settings.html', SETTINGS=SETTINGS,
                                                address = request.host,
                                                start = SETTINGS['COMPETITION_START_TIME']['value'].isoformat(),
                                                tick = SETTINGS['GAME_TICK_DURATION']['value']*1000,
                                                api_key = SETTINGS['API_KEY']['value'],
                                                PLUGIN_SETTINGS = plugin.settings)

# -------------------------------------------------------------
# Filter
# -------------------------------------------------------------
@app.route('/group', methods=['GET'])
@auth_service.requires_auth
def group():
    
    # Getting the request data
    data = request.args
    if not data['group']:
        return "No group provided", 400
    
    group = data['group'].lower()

    return jsonify(database_service.filter_query(group)), 200


# -------------------------------------------------------------
# Statistics endpoint
# -------------------------------------------------------------
@app.route('/stats', methods=['GET'])
@auth_service.requires_auth
def stats():
    data = request.args
    group = data.get('group')
    
    if not group:
        return "No group provided", 400
    
    buckets = {}
    flags = database_service.get_all_accepted_rejected()
    
    game_start = SETTINGS['COMPETITION_START_TIME']['value']
    game_tick_duration = SETTINGS['GAME_TICK_DURATION']['value']

    for f in flags:
        seconds_since_gamestart = (f.date - game_start).total_seconds()
        round_num = 1 + seconds_since_gamestart // game_tick_duration

        if round_num not in buckets:
            buckets[round_num] = {}

        group_value = getattr(f, group, None)
        if group_value is None:
            continue

        if group_value not in buckets[round_num]:
            buckets[round_num][group_value] = {"accepted": 0, "rejected": 0}

        if f.status == ACCEPTED:
            buckets[round_num][group_value]["accepted"] += 1
        else:
            buckets[round_num][group_value]["rejected"] += 1
    
    return jsonify(buckets)


# -------------------------------------------------------------
# Info page
# -------------------------------------------------------------
@app.route('/info', methods=['GET'])
@auth_service.requires_auth
def rejected_info():
    data = request.args
    if not data.get('type') or not data.get('value'):
        return "Invalid input", 400

    data_type = data.get('type')
    value = data.get('value')

    return render_template('info.html',
                        address = request.host,
                        start = SETTINGS['COMPETITION_START_TIME']['value'].isoformat(),
                        tick = SETTINGS['GAME_TICK_DURATION']['value']*1000,
                        data_type = data_type.upper(),
                        value = value,
                        api_key = SETTINGS['API_KEY']['value'])


# -------------------------------------------------------------
# Info data
# -------------------------------------------------------------
@app.route('/info_data', methods=['GET'])
@auth_service.requires_auth
def info_data():
    data = request.args
    if not data.get('type') or not data.get('value'):
        return "Invalid input", 400

    data_type = data.get('type')
    value = data.get('value')

    response = [[f.message, f.date, f.flag] for f in database_service.get_rejected(data_type, value)]
    return jsonify(response), 200


# -------------------------------------------------------------
# Main
# -------------------------------------------------------------

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(banner)
    print("Starting the Peaceful Farm server...")
    print("Starting time: ", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print(settings_feedback)

    database_service.wait_for_db_connection()

    # Start the background task in a separate thread
    print("Starting the background task...")
    submission_service.start()
    
    app.run(host='0.0.0.0', port=5000)