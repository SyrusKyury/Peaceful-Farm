from datetime import datetime
import os
import json
import importlib


class SettingsSystem:

    def __init__(self) -> None:
        self.init_settings()
        self.init_constants()


    def init_settings(self):
        self.settings = json.loads(open('settings.json').read())
        self.settings['COMPETITION_START_TIME']['value'] = datetime.strptime(self.settings['COMPETITION_START_TIME']['value'],
                                                                        "%Y-%m-%d %H:%M:%S")
        
        plugin_name = self.get_setting('SUBMISSION_PROTOCOL')
        self.plugin_module = importlib.import_module(f"plugins.{plugin_name}.{plugin_name}")


    def init_constants(self):
            self.constants = {
            'PEACEFUL_FARM_SERVER_PORT': os.getenv('PEACEFUL_FARM_SERVER_PORT', '5000'),

            # ------------------------------------------------------------------------------
            # MySQL connection configuration
            # ------------------------------------------------------------------------------
            'MYSQL_ROOT_PASSWORD': os.getenv('MYSQL_ROOT_PASSWORD', 'root_password'),
            'MYSQL_DATABASE': os.getenv('MYSQL_DATABASE', 'cyber_challenge'),
            'MYSQL_USER': os.getenv('MYSQL_USER', 'napoli'),
            'MYSQL_PASSWORD': os.getenv('MYSQL_PASSWORD', 'forza_napoli'),

            # ------------------------------------------------------------------------------
            # Constants
            # ------------------------------------------------------------------------------
            'CLIENT_TEMPLATE': open('/app/src/utils/client_template.py').read(),
            'PHP_URL' : 'http://php:8000',
            'NODE_URL' : 'http://node:8000',

            # ------------------------------------------------------------------------------
            # Other constants
            # ------------------------------------------------------------------------------
            'PENDING': 0,
            'ACCEPTED': 1,
            'REJECTED': 2
        }

    
    def get_setting(self, key):
        if key not in self.settings:
            return None
        return self.settings[key]['value']
    

    def get_constant(self, key):
        if key not in self.constants:
            return None
        return self.constants[key]
    

    def update_settings(self, new_settings : dict):
        for key in new_settings:
            if key in self.settings:
                self.settings[key]['value'] = new_settings[key]
    

    def update_settings_file(self):
        with open('settings.json', 'w') as f:
            f.write(json.dumps(self.settings, indent=4))


    def sign_up_plugin_attributes(self, auth_service, app):
        self.auth_service = auth_service
        self.app = app
        self.update_plugin()


    def get_plugin_settings_path(self):
        return os.path.join(os.path.join('plugins', self.get_setting('SUBMISSION_PROTOCOL')), 'settings.json')


    def get_plugins_settings(self):
        settings_path : str = self.get_plugin_settings_path()
        plugin_settings : dict = json.loads(open(settings_path).read())
        return plugin_settings


    def update_plugin(self):
        plugin_class : str = self.get_setting('SUBMISSION_PROTOCOL').upper()
        self.plugin = getattr(self.plugin_module, plugin_class)(self.app, self.auth_service, self)

        plugin_settings = self.get_plugins_settings()

        for key, value in plugin_settings.items():
            setattr(self.plugin, key.lower(), value['value'])


    def show(self):
        settings_feedback = f"""
        --------------------------------------------------------------------------------
        Server started with the following settings:
        - FLAGS_SUBMISSION_DEBUG: {self.settings['FLAGS_SUBMISSION_DEBUG']['value']}

        - MYSQL_DATABASE: {self.constants['MYSQL_DATABASE']}
        - MYSQL_USER: {self.constants['MYSQL_USER']}
        - MYSQL_PASSWORD: ********
        - MYSQL_ROOT_PASSWORD: ********

        - GAME_TICK_DURATION: {self.settings['GAME_TICK_DURATION']['value']}
        - FLAGS_SUBMISSION_WINDOW: {self.settings['FLAGS_SUBMISSION_WINDOW']['value']}
        - COMPETITION_START_TIME: {self.settings['COMPETITION_START_TIME']['value'].strftime('%Y-%m-%d %H:%M:%S')}

        - ACCOUNTS: {','.join(a['username'] for a in self.settings['ACCOUNTS']['value'])}
        - API_KEY: {self.settings['API_KEY']['value']}
        - SUBMIT_TIME: {self.settings['SUBMIT_TIME']['value']}

        - PEACEFUL_FARM_SERVER_PORT: {self.constants['PEACEFUL_FARM_SERVER_PORT']}
        """
        print(settings_feedback)