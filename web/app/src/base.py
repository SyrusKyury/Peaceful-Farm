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
from settings import *
from src.database_service import DatabaseService
from src.submission_service import SubmissionService
from src.notification_service import NotificationService
from src.auth_service import AuthService
import importlib
import uuid

plugin_module = importlib.import_module(f"plugins.{SETTINGS['SUBMISSION_PROTOCOL']['value']}.{SETTINGS['SUBMISSION_PROTOCOL']['value']}")

app = Flask(__name__)
app.config['SECRET_KEY'] = str(uuid.uuid4())
socketio = SocketIO(app)

database_service = DatabaseService(app)
notification_service = NotificationService(socketio)
auth_service = AuthService()
plugin = getattr(plugin_module, SETTINGS['SUBMISSION_PROTOCOL']['value'].upper())(app, auth_service)
submission_service = SubmissionService(notification_service, database_service, plugin)