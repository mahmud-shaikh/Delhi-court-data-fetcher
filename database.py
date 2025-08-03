import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_type TEXT,
            case_number TEXT,
            year TEXT,
            response TEXT,
            timestamp TEXT 
        )
    ''')
    conn.commit()
    return conn

def log_query(conn, case_type, case_number, year, response):
    # conn = sqlite3.connect('database.db')
    # c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute("INSERT INTO logs (case_type, case_number, year, response, timestamp) VALUES (?, ?, ?, ?, ?)",
              (case_type, case_number, year, response, timestamp))
    conn.commit()

def close_conn(conn):
    # Close connection
    conn.close()