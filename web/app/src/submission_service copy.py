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
from src.database_service import DatabaseService
from src.notification_service import NotificationService

# -----------------------------------------------------------------------------------
# Background task to submit the flags to the submission server
# -----------------------------------------------------------------------------------

class SubmissionService(threading.Thread):
    """
    This class is a background task that will submit the flags to the submission server.
    """

    def __init__(self, notification_service : NotificationService, database_service : DatabaseService, plugin):
        super().__init__()
        self.notification_service : NotificationService = notification_service
        self.database_service : DatabaseService = database_service
        self.urgent_event : threading.Event = threading.Event()
        self.stop_event : threading.Event = threading.Event()
        self.plugin = plugin

    def run(self):
        game_start = SETTINGS['COMPETITION_START_TIME']['value']
        seconds_since_gamestart: float = (datetime.now() - game_start).total_seconds()
        current_round: int = 1 + seconds_since_gamestart // SETTINGS['GAME_TICK_DURATION']['value']

        if current_round < 0:
            time_to_start : int = (game_start - datetime.now()).total_seconds()

            logging.info("Game has not started yet.")
            logging.info(f"Game will start in {time_to_start} seconds at {game_start.strftime('%Y-%m-%d %H:%M:%S')}")

            time.sleep(time_to_start)

            logging.info("Game started")

        logging.info("Submission service started")

        while not self.stop_event.is_set():

            logging.info(f"Getting ready for round: {current_round}")

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

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logging.info(
                f"[{timestamp}] Waiting {to_wait:.2f} seconds before submitting"
            )

            try:
                self.urgent_event.wait(to_wait)
                self.urgent_event.clear()
            except:
                pass

            if self.stop_event.is_set():
                self.stop_event.clear()
                break

            try:
                self.flag_processing()
            except Exception as e:
                logging.error(f"\t\tError submitting flags: {e}")

            current_round += 1

        logging.info("Submission service stopped")



    def flag_processing(self):
        """
        This function will submit the flags to the submission server, and will update the flags status in the database.
        """

        flags = self.database_service.get_all_pending_flags()

        # If there are no flags to submit, return
        if len(flags) == 0:
            logging.info("No flags to submit")
            return
        logging.info(f"I'm submitting {len(flags)} flags...")

        # Submit the flags with the protocol module
        flags, accepted_flags, rejected_flags = self.plugin.submit_flags(flags)

        # Flags that are still pending
        still_pending = list(filter(lambda x: x.status == PENDING, flags))

        # Remove the pending flags from the list
        flags = list(filter(lambda x: x.status != PENDING, flags))

        # Insert the new flags into the database
        self.database_service.insert_flags(flags)

        # Delete all the pending flags
        self.database_service.clear_pending_flags()

        # Insert the still pending flags into the database
        self.database_service.insert_pending_flags(still_pending)

        msg = f"""
        Submission completed!<br>
        <strong>Submited flags</strong>: {len(flags)}<br>
        <strong>Accepted flags</strong>: {accepted_flags}<br>
        <strong>Rejected flags</strong>: {rejected_flags}<br>
        <strong>Pending flags</strong>: {len(still_pending)}
        """

        self.notification_service.send_notification(msg, "blue")

        # Print the submission results
        logging.info("\t\t" + "-"*50)
        logging.info("\t\tSubmission completed")
        logging.info(f"\t\t{len(flags)} flags submitted")
        logging.info(f"\t\t{accepted_flags} flags accepted")
        logging.info(f"\t\t{rejected_flags} flags rejected")
        logging.info(f"\t\t{len(still_pending)} flags still pending")
        logging.info("\t\t" + "-"*50)


    def stop(self):
        """
        This function will stop the submission service.
        """
        logging.info("Stopping submission service")
        self.stop_event.set()
        self.urgent_event.set()
        self.join()
        logging.info("Submission service stopped")

    
    def urgent(self):
        """
        This function will set the urgent event, to submit the flags immediately.
        """
        self.urgent_event.set()
        logging.info("Urgent submission requested")