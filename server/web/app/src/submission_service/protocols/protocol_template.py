"""
from src.utils.config import SUBMISSION_SERVER_IP, SUBMISSION_SERVER_PORT, SUBMISSION_SERVER_API_ENDPOINT, SUBMISSION_SERVER_TEAM_TOKEN, FLAGS_SUBMISSION_DEBUG, PEACEFUL_FARM_SERVER_PORT, ACCEPTED, REJECTED
from src.classes.flag import Flag
from flask import blueprints, request
import random
import requests
import json

# -----------------------------------------------------------------------------------
# Submit flags function
# -----------------------------------------------------------------------------------

def submit_flags(flags : list[Flag]) -> tuple[list[Flag], int, int]:

    The submit_flags function is responsible for submitting the flags to the submission server.
    To create your own submission protocol, you need to implement this function.
    The submission_service.core will call this function and will pass a list of Flag objects.

    The function should return a tuple containing:
    - a list of Flag objects with the updated status and message
    - the number of accepted flags
    - the number of rejected flags

    return new_flags, accepted_flags, rejected_flags


# -----------------------------------------------------------------------------------
# Blueprint for the debug endpoint
# -----------------------------------------------------------------------------------
# This endpoint is used to debug the submission service, it will receive flags and
# will respond as the submission server would do
# -----------------------------------------------------------------------------------

@blueprints.route('/debug', methods=['POST'])
def debug():
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
    
"""
    