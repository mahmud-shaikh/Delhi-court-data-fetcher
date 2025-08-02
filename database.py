import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_type TEXT,
            case_number TEXT,
            year TEXT,
            response TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_query(case_type, case_number, year, response):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO logs (case_type, case_number, year, response) VALUES (?, ?, ?, ?)",
              (case_type, case_number, year, response))
    conn.commit()
    conn.close()

# Run this once
init_db()