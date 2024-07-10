# --------------------------------------------------------------------------------------------------------------------------
# Desc: This file contains the database connection and the database initialization. The database is used to store the flags 
# submitted by the users. The database is a MySQL database and the connection is established using the Flask-MySQLdb library.
# The database is initialized with the schema.sql file which contains the schema of the database. The database connection is
# checked using the ping method of the MySQL connection object. If the connection is not established, the function waits for
# the connection to be established.
#
# Version: 1.0
# Author: Raffaele D'Ambrosio
# Full Path: server/web/app/src/database/database.py
# Creation Date: 09/07/2024
# --------------------------------------------------------------------------------------------------------------------------

from flask_mysqldb import MySQL
from src.utils.config import MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE
from src.base import app
from time import sleep

app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = MYSQL_USER
app.config['MYSQL_PASSWORD'] = MYSQL_PASSWORD
app.config['MYSQL_DB'] = MYSQL_DATABASE
mysql = MySQL(app)

def initalize_db():
    """
    Initialize the database with the schema.sql file.
    """
    with app.app_context():
        cur = mysql.connection.cursor()
        with open('src/database/schema.sql', 'r') as f:
            schema_sql = f.read()
        try:
            cur.execute(schema_sql)
        except:
            pass
        finally:
            mysql.connection.commit()
            cur.close()


def wait_for_db_connection(self):
    """
    Wait for the database to be ready.
    """
    with self.app.app_context():
        while True:
            try:
                self.mysql.connection.ping()
                print("Connection established")
                break
            except Exception as e:
                sleep(1)