# --------------------------------------------------------------------------------------------------------------------------
# Desc: Protocol class definition for Cyber Challenge Italy (CCIT). It is used to submit flags to the submission server
# It will send a PUT request to the submission server with the flags to submit and will receive the status of the flags.
# 
# Version: 1.2.1
# Author: Raffaele D'Ambrosio
# Full Path: web/app/src/submission_service/protocols/ccit.py
# Creation Date: 09/07/2024
#
# Changelog:
# 1.2.1 -> Added the flag ids endpoint to retrieve the flag ids from the submission server.
# --------------------------------------------------------------------------------------------------------------------------

from settings import *
from src.flag import Flag
from src.utils.auth import requires_api_key
from flask import request, Blueprint
import random
import requests
import json
import os

SETTINGS_PATH = os.path.join('plugins', 'ccit', 'settings.json')
PLUGIN_SETTINGS = None

def init_settings():
    return json.loads(open(SETTINGS_PATH).read())

PLUGIN_SETTINGS = init_settings()
# -----------------------------------------------------------------------------------
# Submit flags function
# -----------------------------------------------------------------------------------
# This function is responsible for submitting the flags to the submission server
# It will send a PUT request to the submission server with the flags to submit
# The submission server will respond with the status of the flags
# -----------------------------------------------------------------------------------

def submit_flags(flags : list[Flag]) -> tuple[list[Flag], int, int]:
    # Convert the flags to a list of only the flag strings
    flags_list = [i.flag for i in flags if i.flag is not None]
    URL = get_url()

    # Send the flags to the submission server
    server_response = requests.put(URL, headers={'X-Team-Token': PLUGIN_SETTINGS['SUBMISSION_SERVER_TEAM_TOKEN']['value']}, json=flags_list).text
    server_response = json.loads(server_response)
    
    updated_flags = []
    accepted_flags = 0

    # Check the server response and update the flags' status and message
    # based on the response
    for res in server_response:
        if 'Accepted' in res['msg']:
            status = ACCEPTED
            accepted_flags += 1
        else:
            status = REJECTED
        
        result_flag = [i for i in flags if i.flag == res['flag']][0]
        result_flag.status = status
        result_flag.message = res['msg']
        updated_flags.append(result_flag)

    rejected_flags = len(flags) - accepted_flags



    return updated_flags, accepted_flags, rejected_flags


# -----------------------------------------------------------------------------------
# Blueprint to get the list of opponents
# -----------------------------------------------------------------------------------
# This endpoint is used to provide the list of opponents to the client
# -----------------------------------------------------------------------------------
PROTOCOL_BLUEPRINT = Blueprint('protocol', __name__)

@PROTOCOL_BLUEPRINT.route('/targets', methods=['GET'])
@requires_api_key
def targets():
    response = [f"10.60.{i}.1" for i in range(PLUGIN_SETTINGS['N_TEAMS']['value'], 0, -1) if i != PLUGIN_SETTINGS['NOP_TEAM_ID']['value'] and i != PLUGIN_SETTINGS['TEAM_ID']['value']]
    return response, 200

#-----------------------------------------------------------------------------------
# Blueprint to get the nop team ip
#-----------------------------------------------------------------------------------
# This endpoint is used to provide the ip of the nop team to the client
#-----------------------------------------------------------------------------------


@PROTOCOL_BLUEPRINT.route('/nop', methods=['GET'])
@requires_api_key
def nop():
    response = [f"10.60.{PLUGIN_SETTINGS['NOP_TEAM_ID']['value']}.1"]
    return response, 200


# -----------------------------------------------------------------------------------
# Blueprint to your own team ip
# -----------------------------------------------------------------------------------
# This endpoint is used to provide the ip of your team to the client
# -----------------------------------------------------------------------------------

@PROTOCOL_BLUEPRINT.route('/own', methods=['GET'])
@requires_api_key
def myteam():
    response = [f"10.60.{PLUGIN_SETTINGS['TEAM_ID']['value']}.1"]
    return response, 200


# -----------------------------------------------------------------------------------
# Blueprint for the debug endpoint
# -----------------------------------------------------------------------------------
# This endpoint is used to debug the submission service, it will receive flags and
# will respond as the submission server would do
# -----------------------------------------------------------------------------------

@PROTOCOL_BLUEPRINT.route('/debug', methods=['PUT'])
def debug():
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
        response[-1]['msg'] = random.choice(response_list[1:]) if random.random() < 0.05 else response_list[0]
        if "X" in response[-1]['msg']:
            random_float = random.uniform(5, 15)
            response[-1]['msg'] = response[-1]['msg'].replace("X",str(round(random_float, 6))) 
        response[-1]['flag'] = flag
        response[-1]['status'] = True if response[-1]['msg'].startswith('Accepted') else False
    return response, 200
    

# -----------------------------------------------------------------------------------
# Blueprint to get the flag ids
# -----------------------------------------------------------------------------------
# This endpoint is used to provide the list of flag ids to the client, it is used
# to learn data to retrieve flags.
# -----------------------------------------------------------------------------------

@PROTOCOL_BLUEPRINT.route('/flagids', methods=['GET'])
@requires_api_key
def flagids():
    if SETTINGS['FLAGS_SUBMISSION_DEBUG']['value']:
        result = {f"dummy_service{i}" : [f"dummy_data{i}_{j}" for j in range(5)] for i in range(5)}
        return result, 200
    
    flagids_result = requests.get(f"http://{PLUGIN_SETTINGS['SUBMISSION_SERVER_IP']['value']}:{PLUGIN_SETTINGS['SUBMISSION_SERVER_PORT']['value']}/flagids").json()
    return flagids_result

# -----------------------------------------------------------------------------------
# Get url 
# -----------------------------------------------------------------------------------
# This function returns the url of the submission server. In the case of the debug mode,
# it will return the url of the debug endpoint.
# -----------------------------------------------------------------------------------

def get_url():
    if SETTINGS['FLAGS_SUBMISSION_DEBUG']['value']:
        url = f"http://localhost:{PEACEFUL_FARM_SERVER_PORT}/debug"
    else:
        url = "http://{ip}:{port}{api_endpoint}".format(ip=PLUGIN_SETTINGS['SUBMISSION_SERVER_IP']['value'], port=PLUGIN_SETTINGS['SUBMISSION_SERVER_PORT']['value'], api_endpoint=PLUGIN_SETTINGS['SUBMISSION_SERVER_API_ENDPOINT']['value'])
    return url
    