import sqlite3
from datetime import datetime

DB_NAME = "dbs_admissions.db"

def init_database():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS applications (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,address TEXT NOT NULL,qualifications TEXT NOT NULL,course TEXT NOT NULL,start_year INTEGER NOT NULL,start_month INTEGER NOT NULL,registration_number TEXT UNIQUE,created_at TEXT NOT NULL)")
    conn.commit()
    conn.close()

def generate_registration_number(app_id, start_year):
    return f"DBS{start_year}-{app_id:04d}"

def add_application(name, address, qualifications, course, start_year, start_month):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    
    created_at = datetime.now().isoformat()
    
    cur.execute("INSERT INTO applications (name, address, qualifications, course, start_year, start_month, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (name, address, qualifications, course, start_year, start_month, created_at))
    
    app_id = cur.lastrowid
    reg_no = generate_registration_number(app_id, start_year)
    
    cur.execute("UPDATE applications SET registration_number = ? WHERE id = ?", (reg_no, app_id))
    
    conn.commit()
    conn.close()
    
    return reg_no

def main():
    init_database()
    
    name = "Wai Aung"
    address = "Dublin 12"
    qualifications = "BSc Computer Science"
    course = "MSc in Cyber Security"
    start_year = 2025
    start_month = 9
    
    reg_no = add_application(name, address, qualifications, course, start_year, start_month)
    
    print(f"Application Added!")
    print(f"Registration Number: {reg_no}")

if __name__ == "__main__":
    main()