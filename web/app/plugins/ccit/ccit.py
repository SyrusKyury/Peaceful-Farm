from src.plugin import Plugin
from src.settings_system import SettingsSystem
from src.auth_service import AuthService
from src.service import Service
from flask import request, Flask
import requests
import json
import random


class CCIT(Plugin): 

    def __init__(self, app : Flask, auth_service : AuthService, settings_system : SettingsSystem):
        Plugin.__init__(self, app, auth_service, settings_system)
        self.accepted = self.settings_system.get_constant('ACCEPTED')
        self.rejected = self.settings_system.get_constant('REJECTED')


    def submit_flags(self, flags):
        # Convert the flags to a list of only the flag strings
        flags_list : list[str] = [i.flag for i in flags if i.flag is not None]
        URL : str = self.get_url()

        # Send the flags to the submission server
        server_response = requests.put(URL, headers={'X-Team-Token': self.submission_server_team_token}, json=flags_list).text
        server_response = json.loads(server_response)
        
        updated_flags = []
        accepted_flags = 0

        # Check the server response and update the flags' status and message
        # based on the response
        for res in server_response:
            if 'Accepted' in res['msg']:
                status = self.accepted
                accepted_flags += 1
            else:
                status = self.rejected
            
            result_flag = [i for i in flags if i.flag == res['flag']][0]
            result_flag.status = status
            result_flag.message = res['msg']
            updated_flags.append(result_flag)

        rejected_flags = len(flags) - accepted_flags

        return updated_flags, accepted_flags, rejected_flags


    def targets(self):
        response = [f"10.60.{i}.1" for i in range(self.n_teams, 0, -1) if i != self.nop_team_id and i != self.team_id]
        return response, 200

    def nop(self):
        response = [f"10.60.{self.nop_team_id}.1"]
        return response, 200

    def my_team(self):
        response = [f"10.60.{self.team_id}.1"]
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
        flags_submission_debug = self.settings_system.get_setting('FLAGS_SUBMISSION_DEBUG')
        if flags_submission_debug:
            result = {f"dummy_service{i}" : [f"dummy_data{i}_{j}" for j in range(5)] for i in range(5)}
            return result, 200
        
        flagids_result = requests.get(f"http://{self.submission_server_ip}:{self.submission_server_port}/flagids").json()
        return flagids_result, 200


    def get_url(self):
        peaceful_farm_server_port = self.settings_system.get_constant('PEACEFUL_FARM_SERVER_PORT')
        flags_submission_debug = self.settings_system.get_setting('FLAGS_SUBMISSION_DEBUG')

        if flags_submission_debug:
            url = f"http://localhost:{peaceful_farm_server_port}/debug"
        else:
            url = "http://{ip}:{port}{api_endpoint}".format(
                ip=self.submission_server_ip,
                port=self.submission_server_port,
                api_endpoint=self.submission_server_api_endpoint)
        return url