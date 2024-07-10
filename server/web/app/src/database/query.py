# --------------------------------------------------------------------------------------------------------------------------
# Desc: This file contains the database queries. The queries are used to interact with the database. The queries are used to:
# - Get all the pending flags (get_all_prending_flags)
# - Insert flags into the flags table (insert_flags)
# - Clear all the pending flags (clear_pending_flags)
# - Insert pending flags into pending_flags table (insert_pending_flags)
# - Get all the flags + pending flags (get_all_flags)
# - Filter the flags based on a group (filter_query)
# - Get the stats for a specific type and value (stats_query) 
#
# Version: 1.0
# Author: Raffaele D'Ambrosio
# Full Path: server/web/app/src/database/query.py
# Creation Date: 09/07/2024
# --------------------------------------------------------------------------------------------------------------------------
from src.database.database import mysql
from src.classes.flag import Flag
from src.base import app
from datetime import datetime

def get_all_prending_flags():
    with app.app_context():
        # Connect to the database
        cur = mysql.connection.cursor()

        # Get all the pending flags
        cur.execute('''SELECT * FROM pending_flags''')
        flags = cur.fetchall()
        cur.close()

    # Return a list of Flag objects
    return [Flag(query_result=i) for i in flags]


def insert_flags(flags : list[Flag]):
    # If there are no flags to insert, return
    if len(flags) == 0:
        return

    # If there is only one flag, convert it to a list
    if flags.__class__ == Flag:
        flags = [flags]
    
    with app.app_context():
        # Connect to the database
        cur = mysql.connection.cursor()

        # Insert the flags
        cur.executemany('''INSERT IGNORE INTO flags (flag, service, exploit, nickname, ip, date, status, message) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''', [i.to_list() for i in flags])
        mysql.connection.commit()
        cur.close()


def clear_pending_flags():
    with app.app_context():
        # Connect to the database
        cur = mysql.connection.cursor()

        # Delete all the pending flags
        cur.execute('''DELETE FROM pending_flags''')
        mysql.connection.commit()
        cur.close()


def insert_pending_flags(flags : list[Flag]):
    # If there are no flags to insert, return
    if len(flags) == 0:
        return

    # If there is only one flag, convert it to a list
    if flags.__class__ == Flag:
        flags = [flags]
    
    with app.app_context():
        # Connect to the database
        cur = mysql.connection.cursor()

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
        mysql.connection.commit()
        cur.close()
    
def get_all_flags():
    with app.app_context():
        # Connect to the database
        cur = mysql.connection.cursor()

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
    

def filter_query(group : str, t1 : datetime, t2 : datetime) -> list[Flag]:
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
    WHERE date BETWEEN '{t1}' AND '{t2}'
    GROUP BY {group};"""

    with app.app_context():
        # Connect to the database
        cur = mysql.connection.cursor()

        # Get data
        cur.execute(query)
        data = cur.fetchall()
        cur.close()
        return data
    

def stats_query(t1 : datetime, t2 : datetime, type : str, value : str) -> list[Flag]:
    query = f"""
    SELECT {type},date,status,message,flag FROM flags where date BETWEEN '{t1}' AND '{t2}' AND {type} = '{value}' ORDER BY date;"""

    with app.app_context():
        # Connect to the database
        cur = mysql.connection.cursor()

        # Get data
        cur.execute(query)
        data = cur.fetchall()
        data = [Flag(dictionary={f"{type}": i[0], "date": i[1], "status": i[2], "message": i[3], "flag": i[4]}) for i in data]
        cur.close()
        return data