# --------------------------------------------------------------------------------------------------------------------------
# Desc: Protocol class definition for Cyber Challenge Italy (CCIT). It is used to submit flags to the submission server
# It will send a PUT request to the submission server with the flags to submit and will receive the status of the flags.
# 
# Version: 1.2
# Author: Raffaele D'Ambrosio
# Full Path: web/app/src/submission_service/protocols/ccit.py
# Creation Date: 09/07/2024
# --------------------------------------------------------------------------------------------------------------------------

from settings import FLAGS_SUBMISSION_DEBUG, PEACEFUL_FARM_SERVER_PORT, ACCEPTED, REJECTED
from src.flag import Flag
from src.utils.auth import requires_api_key
from flask import Blueprint

# -----------------------------------------------------------------------------------
# Submit flags function
# -----------------------------------------------------------------------------------
# This function is responsible for submitting the flags to the submission server
# It will send a PUT request to the submission server with the flags to submit
# The submission server will respond with the status of the flags
# -----------------------------------------------------------------------------------

def submit_flags(flags : list[Flag]) -> tuple[list[Flag], int, int]:
    raise NotImplementedError
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
    raise NotImplementedError

#-----------------------------------------------------------------------------------
# Blueprint to get the nop team ip
#-----------------------------------------------------------------------------------
# This endpoint is used to provide the ip of the nop team to the client
#-----------------------------------------------------------------------------------


@PROTOCOL_BLUEPRINT.route('/nop', methods=['GET'])
@requires_api_key
def nop():
    raise NotImplementedError


# -----------------------------------------------------------------------------------
# Blueprint to your own team ip
# -----------------------------------------------------------------------------------
# This endpoint is used to provide the ip of your team to the client
# -----------------------------------------------------------------------------------

@PROTOCOL_BLUEPRINT.route('/own', methods=['GET'])
@requires_api_key
def myteam():
    raise NotImplementedError


# -----------------------------------------------------------------------------------
# Blueprint for the debug endpoint
# -----------------------------------------------------------------------------------
# This endpoint is used to debug the submission service, it will receive flags and
# will respond as the submission server would do
# -----------------------------------------------------------------------------------

@PROTOCOL_BLUEPRINT.route('/debug', methods=['PUT'])
def debug():
    raise NotImplementedError
    

# -----------------------------------------------------------------------------------
# Blueprint to get the flag ids
# -----------------------------------------------------------------------------------
# This endpoint is used to provide the list of flag ids to the client, it is used
# to learn data to retrieve flags.
# -----------------------------------------------------------------------------------

@PROTOCOL_BLUEPRINT.route('/flagids', methods=['GET'])
@requires_api_key
def flagids():
    raise NotImplementedError
    