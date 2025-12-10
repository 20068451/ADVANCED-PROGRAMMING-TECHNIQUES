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

def check_auth(req):
    auth_header = req.headers.get("Authorization", "")
    if auth_header == f"Bearer {SIMPLE_TOKEN}":
        return None
    return jsonify({"error": "Unauthorized"}), 401

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

@app.route("/employees", methods=["GET"])
def get_employees():
    auth_err = check_auth(request)
    if auth_err:
        return auth_err

    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT employee_id, name, department, position, status
            FROM employees
            ORDER BY employee_id
            """
        )
        rows = cur.fetchall()

    employees = []
    for r in rows:
        employees.append(
            {
                "employee_id": r[0],
                "name": r[1],
                "department": r[2],
                "position": r[3],
                "status": r[4],
            }
        )

    return jsonify({"employees": employees})

@app.route("/assets", methods=["GET"])
def get_assets():
    auth_err = check_auth(request)
    if auth_err:
        return auth_err

    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT a.asset_id,
                   a.asset_name,
                   a.asset_type,
                   a.status,
                   a.assigned_to,
                   e.name AS employee_name
            FROM assets a
            LEFT JOIN employees e
              ON a.assigned_to = e.employee_id
            ORDER BY a.asset_id
            """
        )
        rows = cur.fetchall()

    assets = []
    for r in rows:
        assets.append(
            {
                "asset_id": r[0],
                "asset_name": r[1],
                "asset_type": r[2],
                "status": r[3],
                "assigned_to": r[4],
                "employee_name": r[5],
            }
        )

    return jsonify({"assets": assets})

if __name__ == "__main__":
    app.run(debug=True)
