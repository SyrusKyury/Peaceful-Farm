# --------------------------------------------------------------------------------------------------------------------------
# Desc: Protocol class definition for Cyber Challenge Italy (CCIT). It is used to submit flags to the submission server
# It will send a PUT request to the submission server with the flags to submit and will receive the status of the flags.
# 
# Version: 1.0
# Author: Raffaele D'Ambrosio
# Full Path: server/web/app/src/submission_service/protocols/ccit.py
# Creation Date: 09/07/2024
# --------------------------------------------------------------------------------------------------------------------------

from src.utils.config import SUBMISSION_SERVER_IP, SUBMISSION_SERVER_PORT, SUBMISSION_SERVER_API_ENDPOINT, SUBMISSION_SERVER_TEAM_TOKEN, FLAGS_SUBMISSION_DEBUG, PEACEFUL_FARM_SERVER_PORT, ACCEPTED, REJECTED
from src.classes.flag import Flag
from flask import request, Blueprint
import random
import requests
import json

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
    server_response = requests.put(URL, headers={'X-Team-Token': SUBMISSION_SERVER_TEAM_TOKEN}, json=flags_list).text
    server_response = json.loads(server_response)
    
    new_flags = []
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
        new_flags.append(result_flag)

    rejected_flags = len(flags) - accepted_flags

    return new_flags, accepted_flags, rejected_flags


# -----------------------------------------------------------------------------------
# Blueprint for the debug endpoint
# -----------------------------------------------------------------------------------
# This endpoint is used to debug the submission service, it will receive flags and
# will respond as the submission server would do
# -----------------------------------------------------------------------------------
PROTOCOL_BLUEPRINT = Blueprint('protocol', __name__)
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
# Get url 
# -----------------------------------------------------------------------------------
# This function returns the url of the submission server. In the case of the debug mode,
# it will return the url of the debug endpoint.
# -----------------------------------------------------------------------------------

def get_url():
    if FLAGS_SUBMISSION_DEBUG:
        url = f"http://localhost:{PEACEFUL_FARM_SERVER_PORT}/debug"
    else:
        url = "http://{ip}:{port}{api_endpoint}".format(ip=SUBMISSION_SERVER_IP, port=SUBMISSION_SERVER_PORT, api_endpoint=SUBMISSION_SERVER_API_ENDPOINT)
    return url
    