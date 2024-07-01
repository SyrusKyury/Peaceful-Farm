# Client setup
You can customize the `/client/client.py` file by editing the following constants:

- **SERVICE**: The name of service you are exploiting. This parameter is fundamental for the stats recording.
- **EXPLOIT**: Your exploit's name. This parameter is fundamental for the stats recording. 
- **DEBUG**: When this parameter is set to True, the client will test your exploit on the NOP Team only without submitting the flag to the **Peaceful Farm Server**.                   

- **SERVER_IP**: Peaceful Farm Server IP
- **SERVER_PORT** = Peaceful Farm server port
- **API_KEY** = This value is used to authenticate the client. You can find and setup the value of your API_KEY by looking it up into the `/server/.env` file.

- **N_TEAMS**: Number of teams in the competition
- **TEAM_ID**: Your team ID
- **NOP_TEAM_ID**: Team ID of the NOP team
- **FLAG_REGEX**: Regex to validate flags
- **SUBMIT_TIME**: How often to submit flags to the server