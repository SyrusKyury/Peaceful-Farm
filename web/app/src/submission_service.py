# --------------------------------------------------------------------------------------------------------------------------
# Desc: This file contains the background task that will submit the flags to the submission server. The background task
# will submit the flags to the submission server SETTINGS['FLAGS_SUBMISSION_WINDOW'] seconds before the end of the round.
# SETTINGS['FLAGS_SUBMISSION_WINDOW'] seconds before the end of the round, the background task will submit the flags to the submission server
# using the protocol specified in the configuration file.
# Both the SETTINGS['FLAGS_SUBMISSION_WINDOW'] and the submission protocol can be configured in the configuration file.
#
# Version: 1.0
# Author: Raffaele D'Ambrosio
# Full Path: server/web/app/src/submission_service/core.py
# Creation Date: 09/07/2024
# --------------------------------------------------------------------------------------------------------------------------
import logging
import time
import threading
from datetime import datetime, timedelta
from settings import *
import importlib
from src.database import get_all_prending_flags, insert_flags, clear_pending_flags, insert_pending_flags

# Import the submission protocol module
protocol_module = importlib.import_module(f"plugins.{SETTINGS['SUBMISSION_PROTOCOL']['value']}.{SETTINGS['SUBMISSION_PROTOCOL']['value']}")


# -----------------------------------------------------------------------------------
# Background task to submit the flags to the submission server
# -----------------------------------------------------------------------------------

def timed_submission(send, urgent_event : threading.Event, stop_event : threading.Event):
    game_start = SETTINGS['COMPETITION_START_TIME']['value']
    seconds_since_gamestart: float = (datetime.now() - game_start).total_seconds()
    current_round: int = 1 + seconds_since_gamestart // SETTINGS['GAME_TICK_DURATION']['value']

    if current_round < 0:
        logging.info("\t\tGame has not started yet")
        logging.info(f"\t\tGame will start in {game_start - datetime.now()}")
        time.sleep((game_start - datetime.now()).total_seconds())
        logging.info("\t\tGame started")

    logging.info("\t\t" + "-"*50)
    logging.info("\t\tGame information")
    logging.info("\t\t" + "-"*50)
    logging.info(f"\t\tGame started at {game_start}")
    logging.info(f"\t\tCurrent round: {current_round}")
    logging.info("\t\t" + "-"*50 + "\n\n\n\n")

    while True:
        next_round_seconds_offset = SETTINGS['GAME_TICK_DURATION']['value'] * current_round
        minutes, seconds = divmod(next_round_seconds_offset, 60)
        hours, minutes = divmod(minutes, 60)
        next_round_diff: float = timedelta(
            hours=hours, minutes = minutes, seconds=seconds
        )
        seconds_until_next_round = (
            game_start + next_round_diff - datetime.now()
        ).total_seconds()

        to_wait = seconds_until_next_round - SETTINGS['FLAGS_SUBMISSION_WINDOW']['value']

        if to_wait < 0:
            to_wait = 0

        timestamp = datetime.now().time().replace(microsecond=0)
        logging.info(
            f"\t\t[{timestamp}] Waiting {to_wait:.2f} seconds before submitting"
        )

        try:
            urgent_event.wait(to_wait)
        except:
            pass
        
        urgent_event.clear()
        if stop_event.is_set():
            return
        
        try:
            flag_processing(send)
        except Exception as e:
            logging.error(f"\t\tError submitting flags: {e}")

        time.sleep(SETTINGS['FLAGS_SUBMISSION_WINDOW']['value'] + 5)
        current_round += 1


def flag_processing(send):
    flags = get_all_prending_flags()

    # If there are no flags to submit, return
    if len(flags) == 0:
        logging.info("\t\tNo flags to submit")
        return
    logging.info(f"\t\tI'm submitting {len(flags)} flags...")

    # Submit the flags with the protocol module
    flags, accepted_flags, rejected_flags = protocol_module.submit_flags(flags)

    # Flags that are still pending
    still_pending = list(filter(lambda x: x.status == PENDING, flags))

    # Remove the pending flags from the list
    flags = list(filter(lambda x: x.status != PENDING, flags))

    # Insert the new flags into the database
    insert_flags(flags)

    # Delete all the pending flags
    clear_pending_flags()

    # Insert the still pending flags into the database
    insert_pending_flags(still_pending)

    msg = f"""
    Submission completed!<br>
    <strong>Submited flags</strong>: {len(flags)}<br>
    <strong>Accepted flags</strong>: {accepted_flags}<br>
    <strong>Rejected flags</strong>: {rejected_flags}<br>
    <strong>Pending flags</strong>: {len(still_pending)}
    """
    send(msg, "blue")

    # Print the submission results
    logging.info("\t\t" + "-"*50)
    logging.info("\t\tSubmission completed")
    logging.info(f"\t\t{len(flags)} flags submitted")
    logging.info(f"\t\t{accepted_flags} flags accepted")
    logging.info(f"\t\t{rejected_flags} flags rejected")
    logging.info(f"\t\t{len(still_pending)} flags still pending")
    logging.info("\t\t" + "-"*50)
