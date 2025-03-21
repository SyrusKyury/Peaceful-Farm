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
from src.flag import Flag
from flask import Flask
from src.auth_service import AuthService
from src.settings_system import SettingsSystem


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


    def __init__(self, app: Flask, auth_service: AuthService, settings_system: SettingsSystem):
        """
        Initializes the Plugin instance with application and authentication service.

        :param app: Flask application instance.
        :param auth_service: AuthService instance for handling API key validation.
        """
        self.app: Flask = app
        self.auth_service: AuthService = auth_service
        self.settings_system: SettingsSystem = settings_system
        self.init_routes()


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
        Initializes the routes for the plugin and updates them if they already exist.
        """
        routes = {
            '/targets': self.targets,
            '/nop': self.nop,
            '/my_team': self.my_team,
            '/debug': self.debug,
            '/flagids': self.flagids
        }

        for route, func in routes.items():
            endpoint = route.strip("/")  # Flask's default endpoint naming

            if endpoint in self.app.view_functions:
                # Modify the existing route's function
                self.app.view_functions[endpoint] = func
            else:
                # Add new route
                methods = ['PUT'] if route == '/debug' else ['GET']
                self.app.add_url_rule(route, endpoint, func, methods=methods)

            # Ensure authentication is applied
            if route != '/debug':
                self.app.view_functions[endpoint] = self.auth_service.requires_api_key(self.app.view_functions[endpoint])




            