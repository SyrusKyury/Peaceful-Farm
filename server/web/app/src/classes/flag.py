# --------------------------------------------------------------------------------------------------------------------------
# Desc: Flag class definition. It is used to store the information of a flag submission and to give a structure to the data
# for a better management of the flags in the database.
#
# Version: 1.0
# Author: Raffaele D'Ambrosio
# Full Path: server/web/app/src/submission_service/flag.py
# Creation Date: 09/07/2024
# --------------------------------------------------------------------------------------------------------------------------
from datetime import datetime

class Flag:

    def __init__(self, flag=None, service=None, exploit=None, nickname=None, ip=None, date=None, status=None, message=None, query_result=None, dictionary=None):
        if query_result:
            # Query result initialization
            self.flag = query_result[0]
            self.service = query_result[1] if len(query_result) >= 2 else None
            self.exploit = query_result[2] if len(query_result) >= 3 else None
            self.nickname = query_result[3] if len(query_result) >= 4 else None
            self.ip = query_result[4] if len(query_result) >= 5 else None
            self.date = query_result[5] if len(query_result) >= 6 else None
            self.status = query_result[6] if len(query_result) >= 7 else 0
            self.message = query_result[7] if len(query_result) >= 8 else None
        elif dictionary:
            self.flag = dictionary['flag']
            self.service = dictionary['service'] if 'service' in dictionary.keys() else None
            self.exploit = dictionary['exploit'] if 'exploit' in dictionary.keys() else None
            self.nickname = dictionary['nickname'] if 'nickname' in dictionary.keys() else None
            self.ip = dictionary['ip'] if 'ip' in dictionary.keys() else None
            self.date = dictionary['date'] if 'date' in dictionary.keys() else None
            self.status = dictionary['status'] if 'status' in dictionary.keys() else 0
            self.message = dictionary['message'] if 'message' in dictionary.keys() else None
        else:
            # Individual fields initialization
            self.flag = flag if flag and len(flag) <= 255 else (flag[:255] if flag else None)
            self.service = service if service and len(service) <= 255 else (service[:255] if service else None)
            self.exploit = exploit if exploit and len(exploit) <= 255 else (exploit[:255] if exploit else None)
            self.nickname = nickname if nickname and len(nickname) <= 255 else (nickname[:255] if nickname else None)
            self.ip = ip if ip and len(ip) <= 255 else (ip[:255] if ip else None)
            self.date = date if date else datetime.now()
            self.status = status if status else 0
            self.message = message if message and len(message) <= 255 else (message[:255] if message else None)


    def to_list(self):
        return [self.flag, self.service, self.exploit, self.nickname, self.ip, self.date, self.status, self.message]
    

    def __str__(self):
        return f"Flag: {self.flag}\nService: {self.service}\nExploit: {self.exploit}\nNickname: {self.nickname}\nIP: {self.ip}\nDate: {self.date}\nStatus: {self.status}\nMessage: {self.message}"
    