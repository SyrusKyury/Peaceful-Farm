# ----------------------------------------------------------------------------------------------------------------------
# Description:
#   The `Plugin` class serves as a base class for defining plugins that interact with a Flask application. Each plugin 
#   extends this class and implements specific functionality such as flag submission, team information, and debugging. 
#   It also handles the configuration loading from a JSON settings file and provides route initialization, 
#   including authentication requirements.
#
#   The class follows the abstract base class pattern, ensuring that subclasses implement essential methods 
#   like submitting flags, fetching target information, and retrieving plugin-specific data.
#
# Version: 1.0
# Author: Raffaele D'Ambrosio
# File Path: web/app/src/plugin.py
# Created On: 02/03/2025
# ----------------------------------------------------------------------------------------------------------------------


import abc
import os
import json
import inspect
from src.flag import Flag
from flask import Flask
from src.auth_service import AuthService
import logging

class Plugin(abc.ABC):
    """
    Base class for defining a plugin that interacts with a web application.
    The Plugin class is abstract and requires subclasses to implement specific functionality.

    Attributes:
        SETTINGS_FILE_NAME (str): The filename for the plugin's settings.
        settings_path (str): The absolute path to the settings file.
        app (Flask): The Flask application instance.
        auth_service (AuthService): The authentication service instance.
        settings (dict): The loaded settings from the JSON file.
    """

    SETTINGS_FILE_NAME: str = 'settings.json'


    def __init__(self, app: Flask, auth_service: AuthService):
        """
        Initializes the Plugin instance with application and authentication service.

        :param app: Flask application instance.
        :param auth_service: AuthService instance for handling API key validation.
        """
        self.settings_path: str = os.path.join(os.path.dirname(inspect.getfile(self.__class__)), self.SETTINGS_FILE_NAME)
        self.app: Flask = app
        self.auth_service: AuthService = auth_service
        self.settings: dict = self.init_settings()
        self.init_routes()


    def init_settings(self) -> dict:
        """
        Loads the settings from the JSON configuration file.

        :return: A dictionary of settings read from the settings file.
        :raises FileNotFoundError: If the settings file does not exist.
        :raises json.JSONDecodeError: If the settings file contains invalid JSON.
        """
        try:
            with open(self.settings_path, 'r') as f:
                settings = json.load(f)
            return settings
        except FileNotFoundError:
            logging.error(f"Settings file not found at {self.settings_path}")
            raise
        except json.JSONDecodeError:
            logging.error(f"Failed to parse settings file {self.settings_path}. Please check the JSON format.")
            raise


    @abc.abstractmethod
    def submit_flags(self, flags: list[Flag]) -> tuple[list[Flag], int, int]:
        """
        Submits flags to the submission endpoint.

        :param flags: List of Flag objects to submit.
        :return: A tuple containing:
        1. The list of flags the system didn't succeed to submit as Flag objects.
        2. The number of accepted flags
        3. The number of rejected flags
        """
        pass


    @abc.abstractmethod
    def targets(self):
        """
        Returns the targets' ip addresses. This function will be called by the /targets route
        and must return the following tuple:

        (list[str], int): A tuple containing a list of target IP addresses and the HTTP status code.
        """
        pass


    @abc.abstractmethod
    def nop(self):
        """
        Returns the nop team's ip address. This function will be called by the /nop route and must 
        return the following tuple:

        (list[str], int): A tuple containing the nop team address in a list and the HTTP status code.
        """
        pass


    @abc.abstractmethod
    def my_team(self):
        """
        Returns the team's ip address. This function will be called by the /my_team route and must
        return the following tuple:

        (list[str], int): A tuple containing the team address in a list and the HTTP status code.
        """
        pass


    @abc.abstractmethod
    def debug(self):
        """
        Debugging endpoint for the plugin. This function will be called by the /debug route and must
        emulate exactly the expected behavior of the game server.
        """
        pass


    @abc.abstractmethod
    def flagids(self):
        """
        Returns the flag IDs. Flag IDs are data used to help players to write exploits. This function
        provides the interface the client uses to get the flag IDs with the /flagids route.
        The function must return the following tuple:

        (dict, int): A tuple containing a dictionary of flag IDs and the HTTP status code.
        """
        pass


    def init_routes(self):
        """
        Initializes the routes for the plugin and adds authentication middleware.
        This /debug route is specific to the plugin and should be implemented in the subclass
        but since most CTF Frameworks have similar structure, it is implemented here as a
        PUT route.

        Routes added:
            - /targets
            - /nop
            - /my_team
            - /debug (PUT method)
            - /flagids
        """
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


        