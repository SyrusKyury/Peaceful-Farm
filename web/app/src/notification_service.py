# ----------------------------------------------------------------------------------------------------------------------
# Description:
#   NotificationService class for managing real-time notifications to the web client. Uses Flask-SocketIO to emit messages.
#
# Version: 1.0
# Author: Raffaele D'Ambrosio
# File Path: web/app/src/notification_service.py
# Created On: 01/02/2025
# Last Updated: 01/02/2025
#
# ----------------------------------------------------------------------------------------------------------------------


from flask_socketio import SocketIO
import logging

class NotificationService:
    """
    NotificationService manages real-time notifications to the web client using Flask-SocketIO.

    Methods:
        - send_notification(message: str, color: str = "green"): Sends a notification to the client.
        - register_events(): Registers SocketIO event handlers.
    """

    VALID_COLORS = {"green", "red", "blue", "yellow", "orange"}

    def __init__(self, socketio: SocketIO):
        """
        Initializes the NotificationService with a SocketIO instance and registers event handlers.

        - :param socketio: Flask-SocketIO instance for handling real-time communication.
        """
        self.socketio = socketio
        self.register_events()


    def send_notification(self, message: str, color: str = "green"):
        """
        Sends a notification to the web client via SocketIO.

        - :param message: The message to send.
        - :param color: The color of the notification (default: "green").
        """
        if not message:
            logging.warning("Attempted to send an empty notification message.")
            return

        color = color.lower()
        if color not in self.VALID_COLORS:
            logging.warning(f"Invalid color '{color}' used in send_notification. Defaulting to 'green'.")
            color = "green"

        logging.debug(f"Sending notification: {message} (color: {color})")
        self.socketio.emit('message', {'data': message, 'color': color})


    def register_events(self):
        """
        Registers all necessary SocketIO events.
        """
        self.register_connect_event()


    def register_connect_event(self):
        """
        Handles the event when a web client connects.
        """
        @self.socketio.on('connect')
        def handle_connect():
            logging.info("Web client connected to the server.")
