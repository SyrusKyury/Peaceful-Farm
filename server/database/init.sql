GRANT ALL PRIVILEGES ON *.* TO 'napoli'@'%' IDENTIFIED BY 'forza_napoli';
FLUSH PRIVILEGES;

/*
    Creating table with the following data to store accepted and rejected flags
    Flag: flag for the attack defense challenge Primary Key
    Service: service attacked
    Exploit: name of the exploit
    Nickname: nickname of the attacker
    Date: timestamp of the attack (YYYY-MM-DD HH:MM:SS)
    Status: status of the attack int (1: accepted, 2: rejected)
    Message: message from the game server
*/

CREATE TABLE flags (
    flag VARCHAR(255) NOT NULL,
    service VARCHAR(255) NOT NULL,
    exploit VARCHAR(255) NOT NULL,
    nickname VARCHAR(255) NOT NULL,
    ip VARCHAR(255) NOT NULL,
    date TIMESTAMP NOT NULL,
    status INT NOT NULL,
    message TEXT,
    PRIMARY KEY (ip, flag)
);

/*
    Creating table with the following data to store pending flags
    Flag: flag for the attack defense challenge Primary Key
    Service: service attacked
    Exploit: name of the exploit
    Nickname: nickname of the attacker
    Date: timestamp of the attack (YYYY-MM-DD HH:MM:SS)
*/

CREATE TABLE pending_flags (
    flag VARCHAR(255) NOT NULL,
    service VARCHAR(255) NOT NULL,
    exploit VARCHAR(255) NOT NULL,
    nickname VARCHAR(255) NOT NULL,
    ip VARCHAR(255) NOT NULL,
    date TIMESTAMP NOT NULL,
    PRIMARY KEY (flag, ip)
);