import sqlite3
from flask import g
import datetime

# Constants
PENDING = 0
ACCEPTED = 1
REJECTED = 2
a = sqlite3.connect('database.db')

# Creating a connection to the database
def get_db():
    """Get a database connection for the current application context."""
    db = getattr(g, '_database', None)
    try:
        db.cursor()
    except:
        db = g._database = sqlite3.connect('database.db')
    return db

def get_db_cursor():
    """Get a database cursor."""
    conn = get_db()
    return conn.cursor()

def init_db():
    """Initialize the database with the schema."""
    conn = get_db()
    cursor = get_db_cursor()
    with open('src/schema.sql', 'r') as f:
        schema_sql = f.read()
    try:
        cursor.executescript(schema_sql)
        conn.commit()
    except sqlite3.OperationalError as e:
        pass
    finally:
        cursor.close()
        conn.close()


"""
CREATE TABLE flags (
    flag VARCHAR(255) PRIMARY KEY,
    service VARCHAR(255) NOT NULL,
    exploit VARCHAR(255) NOT NULL,
    nickname VARCHAR(255) NOT NULL,
    date TIMESTAMP NOT NULL,
    status INT NOT NULL,
    message TEXT
);
"""

def insert_flag(flag, service, exploit, nickname):
    conn = get_db()
    cursor = get_db_cursor()

    # Getting the current date and time
    date = datetime.datetime.now()
    service = service.upper()
    exploit = exploit.upper()
    nickname = nickname.upper()
    message = None
    status = PENDING
    # Try to insert the flag into the database if it doesn't exist
    try:
        cursor.execute('''INSERT INTO flags (flag, service, exploit, nickname, date, status, message) VALUES (?, ?, ?, ?, ?, ?, ?)''', (flag, service, exploit, nickname, date, status, message))
        conn.commit()
        return 1
    except sqlite3.IntegrityError:
        return 0

def insert_flags(flags : list[str], service : str, exploit : str, nickname : str):
    result = 0
    for flag in flags:
        result += insert_flag(flag, service, exploit, nickname)
    return result

def get_flags():
    cursor = get_db_cursor()
    cursor.execute('''
        SELECT * FROM flags
    ''')
    return cursor.fetchall()

def get_pending_flags():
    cursor = get_db_cursor()
    cursor.execute('''
        SELECT * FROM flags WHERE status = ?
    ''', (PENDING,))
    return cursor.fetchall()

def update_flag_status(flag, status, message=None):
    conn = get_db()
    cursor = get_db_cursor()
    cursor.execute('''
        UPDATE flags SET status = ?, message = ? WHERE flag = ?
    ''', (status, message, flag))
    conn.commit()

