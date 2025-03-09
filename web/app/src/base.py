# --------------------------------------------------------------------------------------------------------------------------
# Desc: This file is responsible for both the initialization of the flask app and the configuration of extra API routes
# specific to the submission protocol. The app is initialized with the Flask library and the API routes are added using the
# blueprint pattern. The blueprint pattern is used to separate the API routes from the main app. The API routes are stored in
# the submission_service/protocols directory. The API routes are added to the app using the register_blueprint method.
#
# Version: 1.0
# Author: Raffaele D'Ambrosio
# Full Path: server/web/app/src/base.py
# Creation Date: 09/07/2024
# --------------------------------------------------------------------------------------------------------------------------
from flask import Flask
from flask_socketio import SocketIO
from src.settings_system import SettingsSystem
from src.database_service import DatabaseService
from src.submission_service import SubmissionService
from src.notification_service import NotificationService
from src.auth_service import AuthService
import importlib
import uuid
import os


template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__).split('src')[0], 'frontend', 'templates'))
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__).split('src')[0], 'frontend', 'static'))

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.config['SECRET_KEY'] = str(uuid.uuid4())
socketio = SocketIO(app)

settings_system = SettingsSystem()
database_service = DatabaseService(app, settings_system)
notification_service = NotificationService(socketio, settings_system)
auth_service = AuthService(settings_system)
submission_protocol = settings_system.get_setting('SUBMISSION_PROTOCOL')

plugin_module = importlib.import_module(f"plugins.{submission_protocol}.{submission_protocol}")
plugin = getattr(plugin_module, submission_protocol.upper())(app, auth_service, settings_system)
submission_service = SubmissionService(notification_service, database_service, plugin, settings_system)