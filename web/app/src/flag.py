# ----------------------------------------------------------------------------------------------------------------------
# Description:
#   Flag class definition for managing flag submissions. This class provides a structured representation of flag data 
#   and facilitates interaction with the database.
#
# Version: 1.1
# Author: Raffaele D'Ambrosio
# File Path: web/app/src/submission_service/flag.py
# Created On: 09/07/2024
# Last Updated: 02/03/2025
#
# Changelog:
#   - Improved readability and conciseness of the description.
#   - Changed "manage flag data" → "facilitates interaction with the database" for clarity.
#   - Added "Version 1.1" to reflect updates.
#   - Included "Last Updated" field for better tracking.
#   - Reformatted comments for consistency.
# ----------------------------------------------------------------------------------------------------------------------

from datetime import datetime

class Flag:
    """
    A class representing a flag submission.

    Attributes:
        flag (str): The flag string.
        service (str): The service the flag is related to.
        exploit (str): The exploit used to obtain the flag.
        nickname (str): The nickname of the user who submitted the flag.
        ip (str): The IP address of the server where the flag was found.
        date (datetime): The date and time when the flag was submitted.
        status (int): The status of the flag (0: Pending, 1: Accepted, 2: Rejected).
        message (str, optional): The response message from the submission server.
    
    Alternative Initialization:
        query_result (tuple): Initialize the class with a database query result.
        dictionary (dict): Initialize the class with a dictionary.
    """

    def __init__(
        self, flag=None, service=None, exploit=None, nickname=None, ip=None, 
        date=None, status=None, message=None, query_result=None, dictionary=None
    ):
        if query_result:
            # Initialize from database query result (tuple)
            self.flag = query_result[0]
            self.service = query_result[1] if len(query_result) > 1 else None
            self.exploit = query_result[2] if len(query_result) > 2 else None
            self.nickname = query_result[3] if len(query_result) > 3 else None
            self.ip = query_result[4] if len(query_result) > 4 else None
            self.date = query_result[5] if len(query_result) > 5 else None
            self.status = query_result[6] if len(query_result) > 6 else 0
            self.message = query_result[7] if len(query_result) > 7 else None

        elif dictionary:
            # Initialize from dictionary
            self.flag = dictionary.get('flag')
            self.service = dictionary.get('service')
            self.exploit = dictionary.get('exploit')
            self.nickname = dictionary.get('nickname')
            self.ip = dictionary.get('ip')
            self.date = dictionary.get('date', datetime.now())
            self.status = dictionary.get('status', 0)
            self.message = dictionary.get('message')

        else:
            # Initialize from individual parameters
            self.flag = self._truncate(flag)
            self.service = self._truncate(service)
            self.exploit = self._truncate(exploit)
            self.nickname = self._truncate(nickname)
            self.ip = self._truncate(ip)
            self.date = date if date else datetime.now()
            self.status = status if status is not None else 0
            self.message = self._truncate(message)


    def _truncate(self, value, max_length=255):
        """Helper function to truncate strings to the allowed length."""
        return value[:max_length] if isinstance(value, str) else value


    def to_list(self):
        """Returns the flag attributes as a list for easy database storage."""
        return [self.flag, self.service, self.exploit, self.nickname, self.ip, self.date, self.status, self.message]


    def __str__(self):
        """Returns a string representation of the flag object."""
        return (
            f"Flag: {self.flag}\n"
            f"Service: {self.service}\n"
            f"Exploit: {self.exploit}\n"
            f"Nickname: {self.nickname}\n"
            f"IP: {self.ip}\n"
            f"Date: {self.date}\n"
            f"Status: {self.status}\n"
            f"Message: {self.message}"
        )
