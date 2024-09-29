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
from settings import SUBMISSION_PROTOCOL
import importlib

protocol_module = importlib.import_module('plugins.' + SUBMISSION_PROTOCOL)

app = Flask(__name__)
app.register_blueprint(protocol_module.PROTOCOL_BLUEPRINT)