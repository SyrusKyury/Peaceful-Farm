from src.plugin import Plugin
from settings import ACCEPTED, REJECTED, SETTINGS, PEACEFUL_FARM_SERVER_PORT
from flask import request
import requests
import json
import random


class CCIT(Plugin): 

    def __init__(self, app, auth_service):
        super().__init__(app, auth_service)


    def submit_flags(self, flags):
        # Convert the flags to a list of only the flag strings
        flags_list : list[str] = [i.flag for i in flags if i.flag is not None]
        URL : str = self.get_url()

        # Send the flags to the submission server
        server_response = requests.put(URL, headers={'X-Team-Token': self.settings['SUBMISSION_SERVER_TEAM_TOKEN']['value']}, json=flags_list).text
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


    def targets(self):
        response = [f"10.60.{i}.1" for i in range(self.settings['N_TEAMS']['value'], 0, -1) if i != self.settings['NOP_TEAM_ID']['value'] and i != self.settings['TEAM_ID']['value']]
        return response, 200

    def nop(self):
        response = [f"10.60.{self.settings['NOP_TEAM_ID']['value']}.1"]
        return response, 200

    def my_team(self):
        response = [f"10.60.{self.settings['TEAM_ID']['value']}.1"]
        return response, 200


    def debug(self):
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


    def flagids(self):
        if SETTINGS['FLAGS_SUBMISSION_DEBUG']['value']:
            result = {f"dummy_service{i}" : [f"dummy_data{i}_{j}" for j in range(5)] for i in range(5)}
            return result, 200
        
        flagids_result = requests.get(f"http://{self.settings['SUBMISSION_SERVER_IP']['value']}:{self.settings['SUBMISSION_SERVER_PORT']['value']}/flagids").json()
        return flagids_result


    def get_url(self):
        if SETTINGS['FLAGS_SUBMISSION_DEBUG']['value']:
            url = f"http://localhost:{PEACEFUL_FARM_SERVER_PORT}/debug"
        else:
            url = "http://{ip}:{port}{api_endpoint}".format(ip=self.settings['SUBMISSION_SERVER_IP']['value'], port=self.settings['SUBMISSION_SERVER_PORT']['value'], api_endpoint=self.settings['SUBMISSION_SERVER_API_ENDPOINT']['value'])
        return url