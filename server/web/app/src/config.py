from datetime import datetime
import os

# ------------------------------------------------------------------------------
# Live testing
# ------------------------------------------------------------------------------

FLASK_DEBUG = False
FLAGS_SUBMISSION_DEBUG = False

# ------------------------------------------------------------------------------
# Banner
# ------------------------------------------------------------------------------
    
banner = """
.-------.    ____        _______      .-''-.   ________   ___    _   .---.      
\  _(`)_ \ .'  __ `.    /   __  \   .'_ _   \ |        |.'   |  | |  | ,_|      
| (_ o._)|/   '  \  \  | ,_/  \__) / ( ` )   '|   .----'|   .'  | |,-./  )      
|  (_,_) /|___|  /  |,-./  )      . (_ o _)  ||  _|____ .'  '_  | |\  '_ '`)    
|   '-.-'    _.-`   |\  '_ '`)    |  (_,_)___||_( )_   |'   ( \.-.| > (_)  )    
|   |     .'   _    | > (_)  )  __'  \   .---.(_ o._)__|' (`. _` /|(  .  .-'    
|   |     |  _( )_  |(  .  .-'_/  )\  `-'    /|(_,_)    | (_ (_) _) `-'`-'|___  
/   )     \ (_ o _) / `-'`-'     /  \       / |   |      \ /  . \ /  |        \ 
`---'      '.(_,_).'    `._____.'    `'-..-'  '---'       ``-'`-''   `--------` 
                 ________    ____    .-------.    ,---.    ,---.                
                |        | .'  __ `. |  _ _   \   |    \  /    |                
                |   .----'/   '  \  \| ( ' )  |   |  ,  \/  ,  |                
                |  _|____ |___|  /  ||(_ o _) /   |  |\_   /|  |                
                |_( )_   |   _.-`   || (_,_).' __ |  _( )_/ |  |                
                (_ o._)__|.'   _    ||  |\ \  |  || (_ o _) |  |                
                |(_,_)    |  _( )_  ||  | \ `'   /|  (_,_)  |  |                
                |   |     \ (_ o _) /|  |  \    / |  |      |  |                
                '---'      '.(_,_).' ''-'   `'-'  '--'      '--'                
                                                                                
"""

# ------------------------------------------------------------------------------
# Client template
# ------------------------------------------------------------------------------

CLIENT_TEMPLATE = open('/app/src/client_template.py').read()

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
SUBMISSION_SERVER_IP = os.getenv('SUBMISSION_SERVER_IP', '10.10.0.1')
SUBMISSION_SERVER_PORT = os.getenv('SUBMISSION_SERVER_PORT', '8080')
SUBMISSION_SERVER_API_ENDPOINT = os.getenv('SUBMISSION_SERVER_API_ENDPOINT', '/flags')
SUBMISSION_SERVER_TEAM_TOKEN = os.getenv('SUBMISSION_SERVER_TEAM_TOKEN', '31621d1472825a4339a676b6bcd8d81c')
GAME_TICK_DURATION = int(os.getenv('GAME_TICK_DURATION', 120))
FLAGS_SUBMISSION_WINDOW = int(os.getenv('FLAGS_SUBMISSION_WINDOW', 20))
COMPETITION_START_TIME = [int(i) for i in os.getenv('COMPETITION_START_TIME', '11:00:00').split(':')]

# ------------------------------------------------------------------------------
# Client configuration
# ------------------------------------------------------------------------------

REQUIRE_AUTHENTICATION = os.getenv('REQUIRE_AUTHENTICATION', 'true')
ACCOUNTS = accounts = [{"username": u, "password": p} for u, p in (account.split(':') for account in os.getenv('ACCOUNTS', 'napoli:forzanapoli,test:test123').split(','))]
API_KEY = os.getenv('API_KEY', '1234567890')
FLAG_REGEX = os.getenv('FLAG_REGEX', '^[A-Z0-9]{31}=$')
N_TEAMS = os.getenv('N_TEAMS', 41)
TEAM_ID = os.getenv('TEAM_ID', 39)
NOP_TEAM_ID = os.getenv('NOP_TEAM_ID', 0)
SUBMIT_TIME = os.getenv('SUBMIT_TIME', 30)

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

- SUBMISSION_SERVER_IP: {SUBMISSION_SERVER_IP}
- SUBMISSION_SERVER_PORT: {SUBMISSION_SERVER_PORT}
- SUBMISSION_SERVER_API_ENDPOINT: {SUBMISSION_SERVER_API_ENDPOINT}
- SUBMISSION_SERVER_TEAM_TOKEN: {SUBMISSION_SERVER_TEAM_TOKEN}
- GAME_TICK_DURATION: {GAME_TICK_DURATION}
- FLAGS_SUBMISSION_WINDOW: {FLAGS_SUBMISSION_WINDOW}
- COMPETITION_START_TIME: {datetime.now().replace(hour=int(COMPETITION_START_TIME[0]), minute=COMPETITION_START_TIME[1], second=COMPETITION_START_TIME[2])}

- REQUIRE_AUTHENTICATION: {REQUIRE_AUTHENTICATION}
- ACCOUNTS: {','.join(a['username'] for a in ACCOUNTS)}
- API_KEY: {API_KEY}
- FLAG_REGEX: {FLAG_REGEX}
- N_TEAMS: {N_TEAMS}
- TEAM_ID: {TEAM_ID}
- NOP_TEAM_ID: {NOP_TEAM_ID}
- SUBMIT_TIME: {SUBMIT_TIME}

- PEACEFUL_FARM_SERVER_PORT: {PEACEFUL_FARM_SERVER_PORT}
"""

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------
PENDING = 0
ACCEPTED = 1
REJECTED = 2