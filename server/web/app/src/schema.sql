/*
    Creating table with the following data
    Flag: flag for the attack defense challenge Primary Key
    Service: service attacked
    Exploit: name of the exploit
    Nickname: nickname of the attacker
    Date: timestamp of the attack (YYYY-MM-DD HH:MM:SS)
    Status: status of the attack int (0: pending, 1: accepted, 2: rejected)
    Message: message from the game server
*/

CREATE TABLE flags (
    flag VARCHAR(255) PRIMARY KEY,
    service VARCHAR(255) NOT NULL,
    exploit VARCHAR(255) NOT NULL,
    nickname VARCHAR(255) NOT NULL,
    ip VARCHAR(255) NOT NULL,
    date TIMESTAMP NOT NULL,
    status INT NOT NULL,
    message TEXT
);
