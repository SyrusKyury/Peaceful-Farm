# --------------------------------------------------------------------------------------------------------------------------
# Desc: This file contains the configuration of the server. Most of the configuration is done using environment variables
# that are set in the .env file except for the Live testing variables. The configuration includes:
# - MySQL connection configuration
# - Submission server configuration
# - Client configuration
# - Peaceful Farm server configuration
#
# Version: 1.0
# Author: Raffaele D'Ambrosio
# Full Path: server/web/app/src/utils/config.py
# Creation Date: 09/07/2024
# --------------------------------------------------------------------------------------------------------------------------

from datetime import datetime
import os

# ------------------------------------------------------------------------------
# Live testing
# ------------------------------------------------------------------------------

FLASK_DEBUG = False
FLAGS_SUBMISSION_DEBUG = True

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

# ------------------------------------------------------------------------------
# Client template
# ------------------------------------------------------------------------------

CLIENT_TEMPLATE = open('/app/src/utils/client_template.py').read()

# ------------------------------------------------------------------------------
# MySQL connection configuration
# ------------------------------------------------------------------------------
MYSQL_ROOT_PASSWORD = os.getenv('MYSQL_ROOT_PASSWORD', 'root_password')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'cyber_challenge')
MYSQL_USER = os.getenv('MYSQL_USER', 'napoli')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'forza_napoli')

# ------------------------------------------------------------------------------
# Submission server configuration
# ------------------------------------------------------------------------------
GAME_TICK_DURATION = int(os.getenv('GAME_TICK_DURATION', 120))
FLAGS_SUBMISSION_WINDOW = int(os.getenv('FLAGS_SUBMISSION_WINDOW', 20))
COMPETITION_START_TIME = [int(i) for i in os.getenv('COMPETITION_START_TIME', '11:00:00').split(':')]
SUBMISSION_PROTOCOL = os.getenv('SUBMISSION_PROTOCOL', 'ccit')

# ------------------------------------------------------------------------------
# Client configuration
# ------------------------------------------------------------------------------

REQUIRE_AUTHENTICATION = os.getenv('REQUIRE_AUTHENTICATION', 'true')
ACCOUNTS = accounts = [{"username": u, "password": p} for u, p in (account.split(':') for account in os.getenv('ACCOUNTS', 'napoli:forzanapoli,test:test123').split(','))]
API_KEY = os.getenv('API_KEY', '1234567890')
SUBMIT_TIME = os.getenv('SUBMIT_TIME', 30)
ATTACK_TIME = os.getenv('ATTACK_TIME', 10)

# ------------------------------------------------------------------------------
# Peaceful Farm server configuration
# ------------------------------------------------------------------------------

PEACEFUL_FARM_SERVER_PORT = os.getenv('PEACEFUL_FARM_SERVER_PORT', '5000')

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
# Protocol blueprint
# ------------------------------------------------------------------------------
