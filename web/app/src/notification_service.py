
from flask_socketio import SocketIO
import logging


class NotificationService:
    """
    This class is responsible for sending notifications to the web client. It uses the socketio instance to send messages
    to the web client.
    """

    def __init__(self, socketio: SocketIO):
        self.socketio = socketio
        self.register_events()

    def send_notification(self, message : str, color : str = "green"):
        logging.debug(f"Sending notification: {message}")
        self.socketio.emit('message', {'data': message, 'color': color.lower()})

    def register_events(self):
        @self.socketio.on('connect')
        def handle_connect():
            print("Web client connected")