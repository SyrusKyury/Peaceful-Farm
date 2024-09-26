# --------------------------------------------------------------------------------------------------------------------------
# Desc: Protocol class definition for Cyber Challenge Italy (CCIT). It is used to submit flags to the submission server
# It will send a PUT request to the submission server with the flags to submit and will receive the status of the flags.
# 
# Version: 1.1
# Author: Raffaele D'Ambrosio
# Full Path: server/web/app/src/submission_service/protocols/ccit.py
# Creation Date: 09/07/2024
# --------------------------------------------------------------------------------------------------------------------------

from src.utils.config import FLAGS_SUBMISSION_DEBUG, ACCEPTED, REJECTED
from src.classes.flag import Flag
from flask import  Blueprint
from pwn import *
import requests

# -----------------------------------------------------------------------------------
# Protocol setup
# -----------------------------------------------------------------------------------
#
# IP address of the submission server   
SUBMISSION_SERVER_IP = "submission.faustctf.net"
#
# Port the submission server listens on                           
SUBMISSION_SERVER_PORT = "666"
#
# Regex to validate flags
FLAG_REGEX = "FAUST_[A-Za-z0-9/+]{32}"
#
# Your team ID
TEAM_ID = 715
#
# NOP team ID
NOP_TEAM_ID = 1
#
# Flag IDs
FLAG_IDS = "https://2024.faustctf.net/competition/teams.json"
#
#
# -----------------------------------------------------------------------------------
# Your setup is complete!
# -----------------------------------------------------------------------------------
PROTOCOL_BLUEPRINT = Blueprint('protocol', __name__)
# -----------------------------------------------------------------------------------
# Submit flags function
# -----------------------------------------------------------------------------------
# This function is responsible for submitting the flags to the submission server
# It will send a PUT request to the submission server with the flags to submit
# The submission server will respond with the status of the flags
# -----------------------------------------------------------------------------------

if FLAGS_SUBMISSION_DEBUG:
    print("Flags submission debug mode is not available for this protocol")

def submit_flags(flags : list[Flag]) -> tuple[list[Flag], int, int]:
    ip, port = get_connection_params()

    # Convert the flags to a list of only the flag strings
    flags_list = [i.flag for i in flags if i.flag is not None]

    connection = remote(ip, port)
    connection.recvuntil(b"\n\n")

    # Send the flags
    for flag in flags_list:
        connection.sendline(flag.encode())

    response = connection.recvlines(len(flags_list))
    
    accepted_flags = 0
    rejected_flags = 0

    for line in response:
        flag = line.decode()[:38]
        status = line.decode()[38:].strip()
        if "OK" in status:
            flags[flags_list.index(flag)].status = ACCEPTED
            accepted_flags += 1
        elif not ("ERR" in status):
            flags[flags_list.index(flag)].status = REJECTED
            rejected_flags += 1

    connection.close()
    return flags, accepted_flags, rejected_flags


# -----------------------------------------------------------------------------------
# Blueprint to get the list of opponents
# -----------------------------------------------------------------------------------
# This endpoint is used to provide the list of opponents to the client
# -----------------------------------------------------------------------------------

@PROTOCOL_BLUEPRINT.route('/targets', methods=['GET'])
def targets():
    response, _ = flag_ids()
    targets = [f"fd66:666:{i}::2" for i in response['teams'] if i != TEAM_ID]
    return targets, 200

#-----------------------------------------------------------------------------------
# Blueprint to get the nop team ip
#-----------------------------------------------------------------------------------
# This endpoint is used to provide the ip of the nop team to the client
#-----------------------------------------------------------------------------------

@PROTOCOL_BLUEPRINT.route('/nop', methods=['GET'])
def nop():
    response = [f"fd66:666:{NOP_TEAM_ID}::2"]
    return response, 200

# -----------------------------------------------------------------------------------
# Blueprint to your own team ip
# -----------------------------------------------------------------------------------
# This endpoint is used to provide the ip of your team to the client
# -----------------------------------------------------------------------------------
@PROTOCOL_BLUEPRINT.route('/own', methods=['GET'])
def myteam():
    response = [f"fd66:666:{TEAM_ID}::2"]
    return response, 200

# -----------------------------------------------------------------------------------
# Flag IDS
#-----------------------------------------------------------------------------------
@PROTOCOL_BLUEPRINT.route('/flagids', methods=['GET'])
def flag_ids():
    if FLAGS_SUBMISSION_DEBUG:
        response = {
            "teams": [123, 456, 789],
            "flag_ids": {
                "service1": {
                    "123": ["abc123", "def456"],
                    "789": ["xxx", "yyy"]
                }
            }
        }
    else:
        response = requests.get(FLAG_IDS).json()
    return response, 200

# -----------------------------------------------------------------------------------
# Get url 
# -----------------------------------------------------------------------------------
# This function returns the url of the submission server. In the case of the debug mode,
# it will return the url of the debug endpoint.
# -----------------------------------------------------------------------------------

def get_connection_params():
    ip = SUBMISSION_SERVER_IP
    port = SUBMISSION_SERVER_PORT
    return ip, port
    