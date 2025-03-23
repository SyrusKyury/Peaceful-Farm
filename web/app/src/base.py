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
from flask_login import LoginManager
import secrets
import os


template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__).split('src')[0], 'frontend', 'templates'))
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__).split('src')[0], 'frontend', 'static'))

app = Flask('Peaceful Farm', template_folder=template_dir, static_folder=static_dir)
app.config['SECRET_KEY'] = secrets.token_hex()
socketio = SocketIO(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

settings_system = SettingsSystem()
database_service = DatabaseService(app, settings_system)
notification_service = NotificationService(socketio, settings_system)

auth_service = AuthService(settings_system)
settings_system.sign_up_plugin_attributes(auth_service, app)

submission_service = SubmissionService(notification_service, database_service, settings_system)

@login_manager.user_loader
def load_user(user_id):
    return auth_service.load_user(user_id)
