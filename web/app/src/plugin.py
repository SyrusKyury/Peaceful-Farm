import abc
import os
import json
import inspect
from src.flag import Flag
from flask import Flask
from src.auth_service import AuthService

class Plugin(abc.ABC):

    SETTINGS_FILE_NAME : str = 'settings.json'


    def __init__(self, app : Flask, auth_service : AuthService):
        self.settings_path : str = os.path.join(os.path.dirname(inspect.getfile(self.__class__)), self.SETTINGS_FILE_NAME)
        self.app : Flask = app
        self.auth_service : AuthService = auth_service
        self.settings : dict = self.init_settings() 
        self.init_routes()


    def init_settings(self) -> dict:
        return json.loads(open(self.settings_path).read())
    

    @abc.abstractmethod
    def submit_flags(self, flags : list[Flag]) -> tuple[list[Flag], int, int]:
        pass


    @abc.abstractmethod
    def targets(self):
        pass


    @abc.abstractmethod
    def nop(self):
        pass


    @abc.abstractmethod
    def my_team(self):
        pass


    @abc.abstractmethod
    def debug(self):
        pass


    @abc.abstractmethod
    def flagids(self):
        pass


    @abc.abstractmethod
    def get_url(self) -> str:
        pass

    
    def init_routes(self):
        self.app.add_url_rule('/targets', 'targets', self.targets)
        self.app.add_url_rule('/nop', 'nop', self.nop)
        self.app.add_url_rule('/my_team', 'my_team', self.my_team)
        self.app.add_url_rule('/debug', 'debug', self.debug, methods=['PUT'])
        self.app.add_url_rule('/flagids', 'flagids', self.flagids)

        # Add authentication decorator to the routes
        self.app.view_functions['targets'] = self.auth_service.requires_api_key(self.app.view_functions['targets'])
        self.app.view_functions['nop'] = self.auth_service.requires_api_key(self.app.view_functions['nop'])
        self.app.view_functions['my_team'] = self.auth_service.requires_api_key(self.app.view_functions['my_team'])
        self.app.view_functions['flagids'] = self.auth_service.requires_api_key(self.app.view_functions['flagids'])


        