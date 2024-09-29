from datetime import datetime
import os
# --------------------------------------------------------------------------------------------------------------------------
# Desc: This file contains the configuration of the server. Every setting can be changed to customize the server behavior.
# Version: 1.1
# Author: Raffaele D'Ambrosio
# Full Path: settings.py
# Creation Date: 29/07/2024
# Last Update: 29/09/2024
#
# Changelog:
# 1.1 -> Moved the settings into a file that can be reached with more ease.
# 1.1 -> Now the settings are printed at the start of the server.
# 1.1 -> Moved the settings into this file instead of the .env file to make the server more portable.
# 1.0 -> Initial version.
# --------------------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Testing Configuration
# ------------------------------------------------------------------------------

# Set to True to enable debug mode for the Flask application.
# WARNING: Do not enable debug mode in competition because it starts
# two threads to submit flags instead of one.
FLASK_DEBUG = False

# Set to True to enable debug mode for flag submission.
# WARNING: Not every plugin supports debug mode.
FLAGS_SUBMISSION_DEBUG = True

# ------------------------------------------------------------------------------
# Submission Server Configuration
# ------------------------------------------------------------------------------

# Duration of each game tick in seconds
GAME_TICK_DURATION = 120

# Time window (in seconds) before the game tick ends to submit flags
FLAGS_SUBMISSION_WINDOW = 20

# Competition start time in the format [hour, minute, second]
COMPETITION_START_TIME = [11, 0, 0]

# Submission protocol (choose any file from the plugins folder)
SUBMISSION_PROTOCOL = "ccit"

# ------------------------------------------------------------------------------
# Client Configuration
# ------------------------------------------------------------------------------

# Toggle authentication requirement for the client
REQUIRE_AUTHENTICATION = True

# List of accounts for client authentication on the web application
ACCOUNTS = [
    {"username": "napoli", "password": "forzanapoli"}
]

# API key to authenticate client submissions to the Peaceful Farm server
API_KEY = "fZgJyPRkyyQ0NzG6DfWzJwkfdgAF2tre"

# Frequency of client flag submissions to the server (in seconds)
SUBMIT_TIME = 30

# Frequency of client attacks on their targets (in seconds)
ATTACK_TIME = 10


# ------------------------------------------------------------------------------
# Configuration end
# ------------------------------------------------------------------------------



# ------------------------------------------------------------------------------
# Environment variables
# ------------------------------------------------------------------------------

PEACEFUL_FARM_SERVER_PORT = os.getenv('PEACEFUL_FARM_SERVER_PORT', '5000')

# ------------------------------------------------------------------------------
# MySQL connection configuration
# ------------------------------------------------------------------------------
MYSQL_ROOT_PASSWORD = os.getenv('MYSQL_ROOT_PASSWORD', 'root_password')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'cyber_challenge')
MYSQL_USER = os.getenv('MYSQL_USER', 'napoli')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'forza_napoli')


# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

CLIENT_TEMPLATE = open('/app/src/utils/client_template.py').read()


# ------------------------------------------------------------------------------
# Settings feedback
# ------------------------------------------------------------------------------
settings_feedback = f"""
--------------------------------------------------------------------------------
Server started with the following settings:
- FLASK_DEBUG: {FLASK_DEBUG}
- FLAGS_SUBMISSION_DEBUG: {FLAGS_SUBMISSION_DEBUG}

- MYSQL_DATABASE: {MYSQL_DATABASE}
- MYSQL_USER: {MYSQL_USER}
- MYSQL_PASSWORD: ********
- MYSQL_ROOT_PASSWORD: ********


- GAME_TICK_DURATION: {GAME_TICK_DURATION}
- FLAGS_SUBMISSION_WINDOW: {FLAGS_SUBMISSION_WINDOW}
- COMPETITION_START_TIME: {datetime.now().replace(hour=int(COMPETITION_START_TIME[0]), minute=COMPETITION_START_TIME[1], second=COMPETITION_START_TIME[2])}

- REQUIRE_AUTHENTICATION: {REQUIRE_AUTHENTICATION}
- ACCOUNTS: {','.join(a['username'] for a in ACCOUNTS)}
- API_KEY: {API_KEY}
- SUBMIT_TIME: {SUBMIT_TIME}

- PEACEFUL_FARM_SERVER_PORT: {PEACEFUL_FARM_SERVER_PORT}
"""

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------
PENDING = 0
ACCEPTED = 1
REJECTED = 2

# ------------------------------------------------------------------------------
# Banner
# ------------------------------------------------------------------------------
    
banner = """
8888888b.                                     .d888          888      
888   Y88b                                   d88P"           888      
888    888                                   888             888      
888   d88P .d88b.   8888b.   .d8888b .d88b.  888888 888  888 888      
8888888P" d8P  Y8b     "88b d88P"   d8P  Y8b 888    888  888 888      
888       88888888 .d888888 888     88888888 888    888  888 888      
888       Y8b.     888  888 Y88b.   Y8b.     888    Y88b 888 888      
888        "Y8888  "Y888888  "Y8888P "Y8888  888     "Y88888 888      
                                                                      
                                                                      
                                                                      
           8888888888                                                 
           888                                                        
           888                                                        
           8888888  8888b.  888d888 88888b.d88b.                      
           888         "88b 888P"   888 "888 "88b                     
           888     .d888888 888     888  888  888                     
           888     888  888 888     888  888  888                     
           888     "Y888888 888     888  888  888                                                                                                     
"""
