# Server setup in depth
To setup the **Peaceful Farm Server** with your custom options you need to edit the `/server/.env` file. Here's a detailed list of every setting you'll find into the file.


### Database Settings:
- **MYSQL_ROOT_PASSWORD**: Root password for MySQL database administration.
- **MYSQL_DATABASE**: Name of the MySQL database used in the application.
- **MYSQL_USER**: Username for accessing the MySQL database.
- **MYSQL_PASSWORD**: Password associated with the MySQL user.

### Submission Server Settings:
- **SUBMISSION_SERVER_IP**: IP address of the submission server.
- **SUBMISSION_SERVER_PORT**: Port number on which the submission server operates.
- **SUBMISSION_SERVER_API_ENDPOINT**: API endpoint URL to submit flags to.
- **SUBMISSION_SERVER_TEAM_TOKEN**: Token or key required for authentication with the submission server.

### Game Settings:
- **GAME_TICK_DURATION**: Duration of each game tick or cycle in the game logic.
- **FLAGS_SUBMISSION_WINDOW**: How many seconds before the next gametick the server will start submitting flags.
- **COMPETITION_START_TIME**: Start time of the competition or game (HH:MM:SS format).

### Authentication and Security Settings:
- **REQUIRE_AUTHENTICATION**: Boolean flag indicating if authentication is required to access the web interface.
- **ACCOUNTS**: Configuration related to user accounts. (Example: user1:pass1,user2:pass2,user3:pass3)
- **API_KEY**: The api key the clients will use to submit flags to the **Peaceful Farm Server**.
- **FLAG_REGEX**: Regular expression pattern for validating flags.
- **N_TEAMS**: Number of teams participating.
- **TEAM_ID**: Identifier for your team to avoid attack yourself.
- **NOP_TEAM_ID**: Identifier for the NOP team.
- **SUBMIT_TIME**: How often clients submit flags to the **Peaceful Farm Server**.

### Additional Server Settings:
- **PEACEFUL_FARM_SERVER_PORT**: Port number used by the **Peaceful Farm Server**.
- **TIME_ZONE**: Time zone setting used by the application.

