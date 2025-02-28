from datetime import datetime
import os
import json
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

def init_settings():
    SETTINGS = json.loads(open('settings.json').read())
    SETTINGS['COMPETITION_START_TIME']['value'] = datetime.strptime(SETTINGS['COMPETITION_START_TIME']['value'],
                                                                    "%Y-%m-%d %H:%M:%S")
    return SETTINGS

SETTINGS = init_settings()
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
- FLASK_DEBUG: {SETTINGS['FLASK_DEBUG']['value']}
- FLAGS_SUBMISSION_DEBUG: {SETTINGS['FLAGS_SUBMISSION_DEBUG']['value']}

- MYSQL_DATABASE: {MYSQL_DATABASE}
- MYSQL_USER: {MYSQL_USER}
- MYSQL_PASSWORD: ********
- MYSQL_ROOT_PASSWORD: ********


- GAME_TICK_DURATION: {SETTINGS['GAME_TICK_DURATION']['value']}
- FLAGS_SUBMISSION_WINDOW: {SETTINGS['FLAGS_SUBMISSION_WINDOW']['value']}
- COMPETITION_START_TIME: {SETTINGS['COMPETITION_START_TIME']['value'].strftime('%Y-%m-%d %H:%M:%S')}

- REQUIRE_AUTHENTICATION: {SETTINGS['REQUIRE_AUTHENTICATION']['value']}
- ACCOUNTS: {','.join(a['username'] for a in SETTINGS['ACCOUNTS']['value'])}
- API_KEY: {SETTINGS['API_KEY']['value']}
- SUBMIT_TIME: {SETTINGS['SUBMIT_TIME']['value']}

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
