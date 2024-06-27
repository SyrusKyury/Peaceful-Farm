import threading
import time
import requests
from src.config import configuration
from src.SQlite import get_pending_flags, update_flag_status, REJECTED, ACCEPTED
import json
from datetime import datetime, timedelta

# -----------------------------------------------------------------------------------
# Timestamp function
# -----------------------------------------------------------------------------------

def timestamp():
    return datetime.now().time().replace(microsecond=0)

# -----------------------------------------------------------------------------------
# Background task
# -----------------------------------------------------------------------------------

GAMETICK_DURATION = configuration["flagServer"]["game_tick_duration"]
FLAGS_SUBMISSION_WINDOW = configuration["flagServer"]["flags_submission_window"]

def background_task(Appcontext):
    game_start = datetime.now().replace(hour=11, minute=0, second=0, microsecond=0)
    seconds_since_gamestart: float = (datetime.now() - game_start).total_seconds()
    current_round: int = 1 + seconds_since_gamestart // GAMETICK_DURATION

    print("-"*50)
    print("Game information")
    print("-"*50)
    print(f"Game started at {game_start}")
    print(f"Current round: {current_round}")
    print("-"*50 + "\n\n\n\n")

    if current_round < 0:
        print("Game has not started yet")
        print(f"Game will start in {game_start - datetime.datetime.now()}")
        time.sleep((game_start - datetime.datetime.now()).total_seconds())
        print("Game started")

    while True:
        next_round_seconds_offset = GAMETICK_DURATION * current_round
        minutes, seconds = divmod(next_round_seconds_offset, 60)
        hours, minutes = divmod(minutes, 60)
        next_round_diff: float = timedelta(
            hours=hours, minutes=minutes, seconds=seconds
        )
        seconds_until_next_round = (
            game_start + next_round_diff - datetime.now()
        ).total_seconds()

        to_wait = seconds_until_next_round - FLAGS_SUBMISSION_WINDOW

        if to_wait < 0:
            to_wait = 0

        print(
            f"[{timestamp()}] Waiting {to_wait:.2f} seconds before submitting"
        )
        time.sleep(to_wait)
        with Appcontext:
            submit_flags()

        time.sleep(FLAGS_SUBMISSION_WINDOW + 5)
        current_round += 1

# -----------------------------------------------------------------------------------
# Start the background task
# -----------------------------------------------------------------------------------

def start_background_task(Appcontext):
    thread = threading.Thread(target=background_task, args=(Appcontext,))
    thread.daemon = True
    thread.start()

# -----------------------------------------------------------------------------------
# Submit flags function
# -----------------------------------------------------------------------------------

def submit_flags():
    flags = [i[0] for i in get_pending_flags()]
    if len(flags) == 0:
        print("No flags to submit")
        return
    
    if len(flags) == 1:
        print(f"I'm submitting 1 flag...")
    else:
        print(f"I'm submitting {len(flags)} flags...")
    
    accepted_flags = 0
    url = "http://{ip}:{port}{api_endpoint}".format(ip=configuration["flagServer"]["ip"], port=configuration["flagServer"]["port"], api_endpoint=configuration["flagServer"]["api_endpoint"])
    result = requests.put(url, headers={'X-Team-Token': configuration["flagServer"]["team_token"]}, json=flags).text
    result = json.loads(result)
    for res in result:
        if 'Accepted' in res['msg']:
            update_flag_status(res['flag'], ACCEPTED, res['msg'])
            accepted_flags += 1
        else:
            update_flag_status(res['flag'], REJECTED, res['msg'])

    print("-"*50)
    print(f"Submitted flags: {len(flags)}")
    print(f"Accepted flags: {accepted_flags}")
    print(f"Rejected flags: {len(flags) - accepted_flags}")
    print("-"*50)