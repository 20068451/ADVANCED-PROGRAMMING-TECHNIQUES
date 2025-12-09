import socket
import json
import sqlite3
from datetime import datetime

HOST = "127.0.0.1"
PORT = 5000
DB_NAME = "dbs_admissions.db"

def init_database():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS applications (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,address TEXT NOT NULL,qualifications TEXT NOT NULL,course TEXT NOT NULL,start_year INTEGER NOT NULL,start_month INTEGER NOT NULL,registration_number TEXT UNIQUE,created_at TEXT NOT NULL)")
    conn.commit()
    conn.close()

def generate_registration_number(app_id, start_year):
    return f"DBS{start_year}-{app_id:04d}"

def save_application(app_data):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    
    now = datetime.now().isoformat()
    
    cur.execute("INSERT INTO applications (name, address, qualifications, course, start_year, start_month, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (app_data["name"], app_data["address"], app_data["qualifications"], 
                 app_data["course"], app_data["start_year"], app_data["start_month"], now))
    
    app_id = cur.lastrowid
    reg_no = generate_registration_number(app_id, app_data["start_year"])
    
    cur.execute("UPDATE applications SET registration_number = ? WHERE id = ?", (reg_no, app_id))
    
    conn.commit()
    conn.close()
    
    return reg_no

def handle_client(client_socket):
    data = client_socket.recv(4096).decode('utf-8')
    app_data = json.loads(data)
    
    reg_no = save_application(app_data)
    
    response = {"status": "ok", "registration_number": reg_no}
    client_socket.send(json.dumps(response).encode('utf-8'))
    
    client_socket.close()

def main():
    init_database()
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)
    
    print(f"Server running on {HOST}:{PORT}")
    
    while True:
        client_socket, address = server.accept()
        print(f"Client connected from {address}")
        handle_client(client_socket)

if __name__ == "__main__":
    main()