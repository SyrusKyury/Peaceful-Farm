import logging
import time
import threading
from datetime import datetime, timedelta
from src.database_service import DatabaseService
from src.notification_service import NotificationService
from src.service import Service
from src.settings_system import SettingsSystem

# -----------------------------------------------------------------------------------
# Background task to submit the flags to the submission server
# -----------------------------------------------------------------------------------

class SubmissionService(threading.Thread, Service):
    """
    This class is a background task that will submit the flags to the submission server.
    """

    def __init__(self, notification_service : NotificationService, database_service : DatabaseService, settings_system : SettingsSystem):
        threading.Thread.__init__(self)
        Service.__init__(self, settings_system)

        self.notification_service : NotificationService = notification_service
        self.database_service : DatabaseService = database_service
        self.urgent_event : threading.Event = threading.Event()
        self.stop_event : threading.Event = threading.Event()


    def update_settings(self):
        self.game_start : datetime = self.settings_system.get_setting('COMPETITION_START_TIME')
        self.game_tick_duration : int = self.settings_system.get_setting('GAME_TICK_DURATION')
        self.flags_submission_window : int = self.settings_system.get_setting('FLAGS_SUBMISSION_WINDOW')


    def run(self):
        while True:
            seconds_since_gamestart: float = (datetime.now() - self.game_start).total_seconds()
            current_round: int = 1 + seconds_since_gamestart // self.game_tick_duration

            if current_round < 0:
                time_to_start : int = (self.game_start - datetime.now()).total_seconds()

                logging.info("Game has not started yet.")
                logging.info(f"Game will start in {time_to_start} seconds at {self.game_start.strftime('%Y-%m-%d %H:%M:%S')}")

                time.sleep(time_to_start)

                logging.info("Game started")
            
            logging.info("Submission service started")

            while not self.stop_event.is_set():
                logging.info(f"Getting ready for round: {current_round}")

                next_round_seconds_offset = self.game_tick_duration * current_round
                minutes, seconds = divmod(next_round_seconds_offset, 60)
                hours, minutes = divmod(minutes, 60)
                next_round_diff: float = timedelta(
                    hours=hours, minutes = minutes, seconds=seconds
                )
                seconds_until_next_round = (
                    self.game_start + next_round_diff - datetime.now()
                ).total_seconds()

                to_wait = seconds_until_next_round - self.flags_submission_window

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
                    break

                try:
                    self.flag_processing()
                except Exception as e:
                    logging.error(f"\t\tError submitting flags: {e}")

                current_round += 1
            
            logging.info("Submission service stopped")

            while self.stop_event.is_set():
                time.sleep(1)


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
        flags, accepted_flags, rejected_flags = self.settings_system.plugin.submit_flags(flags)

        # Flags that are still pending
        still_pending = list(filter(lambda x: x.status == self.settings_system.get_constant('PENDING'), flags))

        # Remove the pending flags from the list
        flags = list(filter(lambda x: x.status != self.settings_system.get_constant('PENDING'), flags))

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

    
    def urgent(self):
        """
        This function will set the urgent event, to submit the flags immediately.
        """
        self.urgent_event.set()
        logging.info("Urgent submission requested")


    def restart(self):
        """
        This function will restart the submission service.
        """
        self.stop_event.clear()
        self.urgent_event.clear()