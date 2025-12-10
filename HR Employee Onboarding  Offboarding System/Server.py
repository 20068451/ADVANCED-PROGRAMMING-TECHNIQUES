from flask import Flask, request, jsonify
import pyodbc
import hashlib

app = Flask(__name__)

CONN_STR = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=WAIAUNG;"
    "DATABASE=OnboardingDB;"
    "Trusted_Connection=yes;"
)

def get_connection():
    return pyodbc.connect(CONN_STR)

SIMPLE_TOKEN = "simple-token"

def hash_password(plain_text: str) -> str:
    return hashlib.sha256(plain_text.encode("utf-8")).hexdigest()

@app.route("/")
def home():
    return "Employee Onboarding/Offboarding API"

@app.route("/health")
def health():
    return "OK"

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "username and password are required"}), 400
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
    if not row:
        return jsonify({"error": "Invalid username or password"}), 401
    stored_hash = row[0]
    if hash_password(password) != stored_hash:
        return jsonify({"error": "Invalid username or password"}), 401
    return jsonify({"token": SIMPLE_TOKEN})

if __name__ == "__main__":
    app.run(debug=True)
