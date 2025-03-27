from flask_mysqldb import MySQL
from flask import Flask
from src.flag import Flag
from src.settings_system import SettingsSystem
from src.service import Service



class DatabaseService(Service):
    """
    This class is responsible for handling all the database operations. It uses the Flask-MySQLdb library to connect to the
    database and execute queries. The class is responsible for inserting flags into the database, getting all the pending flags
    from the database, and updating the status of the flags in the database.
    """

    def __init__(self, app: Flask, settings_system: SettingsSystem) -> None:
        self.app = app
        self.mysql = MySQL(self.app)
        super().__init__(settings_system)


    def update_settings(self):
        self.rejected = self.settings_system.get_constant('REJECTED')
        self.app.config['MYSQL_HOST'] = 'db'
        self.app.config['MYSQL_USER'] = self.settings_system.get_constant('MYSQL_USER')
        self.app.config['MYSQL_PASSWORD'] = self.settings_system.get_constant('MYSQL_PASSWORD')
        self.app.config['MYSQL_DB'] = self.settings_system.get_constant('MYSQL_DATABASE')


    def wait_for_db_connection(self):
        """
        Wait for the database to be ready.
        """
        from time import sleep
        with self.app.app_context():
            while True:
                try:
                    self.mysql.connection.ping()
                    print("Connection established")
                    break
                except Exception as e:
                    sleep(1)


    def get_all_pending_flags(self):
        with self.app.app_context():
            # Connect to the database
            cur = self.mysql.connection.cursor()

            # Get all the pending flags
            cur.execute('''SELECT * FROM pending_flags''')
            flags = cur.fetchall()
            cur.close()

        # Return a list of Flag objects
        return [Flag(query_result=i) for i in flags]


    def insert_flags(self, flags : list[Flag]):
        # If there are no flags to insert, return
        if len(flags) == 0:
            return

        # If there is only one flag, convert it to a list
        if flags.__class__ == Flag:
            flags = [flags]
        
        with self.app.app_context():
            # Connect to the database
            cur = self.mysql.connection.cursor()

            # Insert the flags
            cur.executemany('''INSERT IGNORE INTO flags (flag, service, exploit, nickname, ip, date, status, message) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''', [i.to_list() for i in flags])
            self.mysql.connection.commit()
            cur.close()


    def clear_pending_flags(self):
        with self.app.app_context():
            # Connect to the database
            cur = self.mysql.connection.cursor()

            # Delete all the pending flags
            cur.execute('''DELETE FROM pending_flags''')
            self.mysql.connection.commit()
            cur.close()


    def insert_pending_flags(self, flags : list[Flag]):
        # If there are no flags to insert, return
        if len(flags) == 0:
            return

        # If there is only one flag, convert it to a list
        if flags.__class__ == Flag:
            flags = [flags]
        
        with self.app.app_context():
            # Connect to the database
            cur = self.mysql.connection.cursor()

            # Insert the flags
            cur.executemany('''
            INSERT IGNORE INTO pending_flags (flag, service, exploit, nickname, ip, date)
            SELECT %s, %s, %s, %s, %s, %s
            FROM DUAL
            WHERE NOT EXISTS (
                SELECT 1
                FROM flags
                WHERE flags.ip = %s
                AND flags.flag = %s
            );''', [[i.flag, i.service, i.exploit, i.nickname, i.ip, i.date, i.ip, i.flag] for i in flags])

            inserted = cur.rowcount

            self.mysql.connection.commit()
            cur.close()

            return inserted
        

    def get_all_flags(self):
        with self.app.app_context():
            # Connect to the database
            cur = self.mysql.connection.cursor()

            # Get all the flags
            cur.execute('''
            SELECT * FROM (SELECT flag, service, exploit, nickname, ip, date, status, message FROM flags
            UNION
            SELECT flag, service, exploit, nickname, ip, date, 0 AS status, NULL AS message FROM pending_flags)
            AS all_flags
            ''')
            flags = cur.fetchall()
            cur.close()
            flags = [Flag(query_result=i) for i in flags]
            return flags
        

    def filter_query(self, group : str) -> list[Flag]:
        query = f"""SELECT 
        {group} AS selected_group,
        SUM(CASE WHEN status = 1 THEN 1 ELSE 0 END) AS Accepted,
        SUM(CASE WHEN status = 2 THEN 1 ELSE 0 END) AS Rejected,
        SUM(CASE WHEN status = 0 THEN 1 ELSE 0 END) AS Pending
        FROM (
            SELECT flag, service, exploit, nickname, ip, date, status, message FROM flags
            UNION
            SELECT flag, service, exploit, nickname, ip, date, 0 AS status, NULL AS message FROM pending_flags
        ) AS combined_flags
        GROUP BY {group};"""

        with self.app.app_context():
            # Connect to the database
            cur = self.mysql.connection.cursor()

            # Get data
            cur.execute(query)
            data = cur.fetchall()
            cur.close()
            return data
        

    def get_all_accepted_rejected(self):
        with self.app.app_context():
            # Connect to the database
            cur = self.mysql.connection.cursor()

            # Get all the flags
            cur.execute('SELECT * FROM flags')
            flags = cur.fetchall()
            cur.close()
            flags = [Flag(query_result=i) for i in flags]
            return flags
        

    def get_rejected(self, type : str, value : str):
        with self.app.app_context():
            # Connect to the database
            cur = self.mysql.connection.cursor()

            # Get all the flags
            cur.execute(f"SELECT * FROM flags WHERE {type}='{value}' AND STATUS={self.rejected}")
            flags = cur.fetchall()
            cur.close()
            flags = [Flag(query_result=i) for i in flags]
            return flags
        
