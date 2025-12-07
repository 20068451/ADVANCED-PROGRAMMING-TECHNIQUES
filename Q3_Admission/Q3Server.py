import sqlite3
from datetime import datetime

DB_NAME = "dbs_admissions.db"

def init_database():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS applications (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,address TEXT NOT NULL,qualifications TEXT NOT NULL,course TEXT NOT NULL,start_year INTEGER NOT NULL,start_month INTEGER NOT NULL,registration_number TEXT UNIQUE,created_at TEXT NOT NULL)")
    conn.commit()
    conn.close()
    print(f"[+] Database '{DB_NAME}' created.")

def generate_registration_number(app_id, start_year):
    return f"DBS{start_year}-{app_id:04d}"

if __name__ == "__main__":
    init_database()
    print("Database!")