from flask import Flask, request, jsonify
import pyodbc
import hashlib
from datetime import datetime, date
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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

def check_auth():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return False
    token = auth_header.split(" ", 1)[1].strip()
    return token == SIMPLE_TOKEN

def generate_next_employee_id(cur) -> str:
    cur.execute("SELECT MAX(employee_id) FROM employees WHERE employee_id LIKE '2000-%'")
    row = cur.fetchone()
    max_id = row[0]
    if max_id is None:
        next_num = 1
    else:
        try:
            part = max_id.split("-")[1]
            next_num = int(part) + 1
        except Exception:
            next_num = 1
    return f"2000-{next_num:03d}"

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
        return jsonify({"error": "Username and Password are required"}), 400
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
    if not row:
        return jsonify({"error": "Invalid username or password"}), 401
    stored_hash = row[0]
    if hash_password(password) != stored_hash:
        return jsonify({"error": "Invalid username or password"}), 401
    return jsonify({"token": SIMPLE_TOKEN, "username": username})

@app.route("/employees", methods=["GET"])
def get_employees():
    if not check_auth():
        return jsonify({"error": "Unauthorized"}), 401
    employees = []
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT employee_id, name, date_of_joining, address, ppsn,
                   position, department, status
            FROM employees
            ORDER BY employee_id
        """)
        for row in cur.fetchall():
            employees.append({
                "employee_id": row.employee_id,
                "name": row.name,
                "doj": str(row.date_of_joining),
                "address": row.address,
                "ppsn": row.ppsn,
                "position": row.position,
                "department": row.department,
                "status": row.status
            })
    return jsonify(employees)

@app.route("/assets", methods=["GET"])
def get_assets():
    if not check_auth():
        return jsonify({"error": "Unauthorized"}), 401
    assets = []
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT a.asset_id, a.asset_name, a.asset_type, a.status,
                   a.assigned_to, e.name AS employee_name
            FROM assets a
            LEFT JOIN employees e
              ON a.assigned_to = e.employee_id
            ORDER BY a.asset_id
        """)
        for row in cur.fetchall():
            assets.append({
                "asset_id": row.asset_id,
                "asset_name": row.asset_name,
                "asset_type": row.asset_type,
                "status": row.status,
                "assigned_to_id": row.assigned_to,
                "assigned_to_name": row.employee_name
            })
    return jsonify(assets)

@app.route("/onboard", methods=["POST"])
def onboard():
    if not check_auth():
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json() or {}
    name = data.get("name")
    doj_str = data.get("doj")
    address = data.get("address")
    ppsn = data.get("ppsn")
    position = data.get("position")
    department = data.get("department")
    asset_ids = data.get("asset_ids", [])
    if not all([name, doj_str, address, ppsn, position, department]):
        return jsonify({"error": "Missing required fields"}), 400
    if len(ppsn) != 9 or not ppsn.isdigit():
        return jsonify({"error": "PPSN must be exactly 9 digits."}), 400
    try:
        doj_date = datetime.fromisoformat(doj_str).date()
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400
    if doj_date < date.today():
        return jsonify({"error": "Date of joining cannot be in the past."}), 400
    with get_connection() as conn:
        cur = conn.cursor()
        new_emp_id = generate_next_employee_id(cur)
        cur.execute("""
            INSERT INTO employees
            (employee_id, name, date_of_joining, address, ppsn,
             position, department, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'ACTIVE')
        """, (new_emp_id, name, doj_date, address, ppsn, position, department))
        for a_id in asset_ids:
            cur.execute("""
                UPDATE assets
                SET status = 'Assigned', assigned_to = ?
                WHERE asset_id = ? AND status = 'Available'
            """, (new_emp_id, a_id))
        cur.execute("""
            INSERT INTO activity_log (employee_id, activity_type, department)
            VALUES (?, 'ONBOARD', ?)
        """, (new_emp_id, department))
        conn.commit()
        cur.execute("""
            SELECT employee_id, name, date_of_joining, address, ppsn,
                   position, department, status
            FROM employees
            WHERE employee_id = ?
        """, (new_emp_id,))
        erow = cur.fetchone()
        employee = {
            "employee_id": erow.employee_id,
            "name": erow.name,
            "doj": str(erow.date_of_joining),
            "address": erow.address,
            "ppsn": erow.ppsn,
            "position": erow.position,
            "department": erow.department,
            "status": erow.status
        }
        cur.execute("""
            SELECT asset_id, asset_name, asset_type
            FROM assets
            WHERE assigned_to = ?
        """, (new_emp_id,))
        assigned_assets = []
        for row in cur.fetchall():
            assigned_assets.append({
                "asset_id": row.asset_id,
                "asset_name": row.asset_name,
                "asset_type": row.asset_type
            })
    return jsonify({
        "message": "Employee onboarded successfully",
        "employee": employee,
        "assigned_assets": assigned_assets
    }), 201

@app.route("/offboard", methods=["POST"])
def offboard():
    if not check_auth():
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json() or {}
    employee_id = data.get("employee_id")
    if not employee_id:
        return jsonify({"error": "employee_id is required"}), 400
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT employee_id, name, date_of_joining, address, ppsn,
                   position, department, status
            FROM employees
            WHERE employee_id = ?
        """, (employee_id,))
        erow = cur.fetchone()
        if not erow:
            return jsonify({"error": "Employee not found"}), 404
        department = erow.department
        cur.execute("""
            SELECT asset_id, asset_name, asset_type
            FROM assets
            WHERE assigned_to = ?
        """, (employee_id,))
        released_assets = []
        for row in cur.fetchall():
            released_assets.append({
                "asset_id": row.asset_id,
                "asset_name": row.asset_name,
                "asset_type": row.asset_type
            })
        cur.execute("""
            UPDATE assets
            SET status = 'Available', assigned_to = NULL
            WHERE assigned_to = ?
        """, (employee_id,))
        cur.execute(
            "UPDATE employees SET status = 'OFFBOARDED' WHERE employee_id = ?",
            (employee_id,)
        )
        cur.execute("""
            INSERT INTO activity_log (employee_id, activity_type, department)
            VALUES (?, 'OFFBOARD', ?)
        """, (employee_id, department))
        conn.commit()
        employee = {
            "employee_id": erow.employee_id,
            "name": erow.name,
            "doj": str(erow.date_of_joining),
            "address": erow.address,
            "ppsn": erow.ppsn,
            "position": erow.position,
            "department": erow.department,
            "status": "OFFBOARDED"
        }
    return jsonify({
        "message": "Employee offboarded successfully",
        "employee": employee,
        "released_assets": released_assets
    })

@app.route("/report/monthly", methods=["GET"])
def monthly_report():
    if not check_auth():
        return jsonify({"error": "Unauthorized"}), 401
    year_str = request.args.get("year")
    month_str = request.args.get("month")
    if not year_str or not month_str:
        return jsonify({"error": "year and month are required"}), 400
    try:
        year = int(year_str)
        month = int(month_str)
    except ValueError:
        return jsonify({"error": "year and month must be integers"}), 400
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT COUNT(*)
            FROM activity_log
            WHERE activity_type = 'ONBOARD'
              AND YEAR(activity_time) = ?
              AND MONTH(activity_time) = ?
        """, (year, month))
        onboarded = cur.fetchone()[0]
        cur.execute("""
            SELECT COUNT(*)
            FROM activity_log
            WHERE activity_type = 'OFFBOARD'
              AND YEAR(activity_time) = ?
              AND MONTH(activity_time) = ?
        """, (year, month))
        offboarded = cur.fetchone()[0]
        cur.execute("""
            SELECT department,
                   SUM(CASE WHEN activity_type = 'ONBOARD' THEN 1 ELSE 0 END) AS onboarded,
                   SUM(CASE WHEN activity_type = 'OFFBOARD' THEN 1 ELSE 0 END) AS offboarded
            FROM activity_log
            WHERE YEAR(activity_time) = ?
              AND MONTH(activity_time) = ?
            GROUP BY department
        """, (year, month))
        by_dept = []
        for row in cur.fetchall():
            by_dept.append({
                "department": row.department,
                "onboarded": row.onboarded,
                "offboarded": row.offboarded
            })
    return jsonify({
        "year": year,
        "month": month,
        "onboarded_count": onboarded,
        "offboarded_count": offboarded,
        "by_department": by_dept
    })

@app.route("/stats", methods=["GET"])
def get_stats():
    if not check_auth():
        return jsonify({"error": "Unauthorized"}), 401
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM employees WHERE status = 'ACTIVE'")
        active_employees = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM assets")
        total_assets = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM assets WHERE status = 'Available'")
        available_assets = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM assets WHERE status = 'Assigned'")
        assigned_assets = cur.fetchone()[0]
        today = date.today()
        cur.execute("""
            SELECT 
                SUM(CASE WHEN activity_type = 'ONBOARD' THEN 1 ELSE 0 END),
                SUM(CASE WHEN activity_type = 'OFFBOARD' THEN 1 ELSE 0 END)
            FROM activity_log
            WHERE YEAR(activity_time) = ? AND MONTH(activity_time) = ?
        """, (today.year, today.month))
        row = cur.fetchone()
        monthly_onboarded = row[0] or 0
        monthly_offboarded = row[1] or 0
    return jsonify({
        "active_employees": active_employees,
        "total_assets": total_assets,
        "available_assets": available_assets,
        "assigned_assets": assigned_assets,
        "monthly_onboarded": monthly_onboarded,
        "monthly_offboarded": monthly_offboarded
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
