import requests
from datetime import datetime, date
from getpass import getpass

BASE_URL = "http://127.0.0.1:5000"
auth_token = None

def get_headers():
    headers = {"Content-Type": "application/json"}
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"
    return headers

def login():
    global auth_token
    print("\n=== HR Login ===")
    username = input("Username: ")
    password = getpass("Password: ")
    data = {"username": username, "password": password}
    try:
        r = requests.post(f"{BASE_URL}/login", json=data)
    except Exception as e:
        print("Error connecting to server:", e)
        return False
    if r.status_code == 200:
        body = r.json()
        token = body.get("token")
        if token:
            auth_token = token
            print("Login successful.")
            return True
    print("Login failed:", r.text)
    return False

def ensure_logged_in():
    if auth_token is None:
        print("You must log in first.")
        return False
    return True

def fetch_assets():
    try:
        r = requests.get(f"{BASE_URL}/assets", headers=get_headers())
    except Exception as e:
        print("Error connecting to server:", e)
        return None
    if r.status_code != 200:
        print("Failed to get assets:", r.text)
        return None
    return r.json()

def fetch_employees():
    try:
        r = requests.get(f"{BASE_URL}/employees", headers=get_headers())
    except Exception as e:
        print("Error connecting to server:", e)
        return None
    if r.status_code != 200:
        print("Failed to get employees:", r.text)
        return None
    return r.json()

def show_available_assets():
    assets = fetch_assets()
    if assets is None:
        return []
    available = [a for a in assets if a.get("status") == "Available"]
    laptop_count = sum(1 for a in available if a.get("asset_type") == "Laptop")
    phone_count = sum(1 for a in available if a.get("asset_type") == "Phone")
    print("\nAvailable assets:")
    print(f"Laptops: {laptop_count}")
    print(f"Phones : {phone_count}")
    if not available:
        print("No assets available.")
        return []
    for a in available:
        print(
            f"ID: {a.get('asset_id')} | "
            f"Name: {a.get('asset_name')} | "
            f"Type: {a.get('asset_type')}"
        )
    return available

def onboard_employee():
    if not ensure_logged_in():
        return
    print("\n=== Onboard New Employee ===")
    name = input("Full name: ")
    while True:
        doj = input("Date of joining (YYYY-MM-DD, today or future): ").strip()
        try:
            doj_date = datetime.fromisoformat(doj).date()
        except ValueError:
            print("Invalid date format.")
            continue
        if doj_date < date.today():
            print("Date of joining cannot be in the past.")
            continue
        break
    address = input("Address: ")
    while True:
        ppsn = input("PPSN (9 digits): ").strip()
        if len(ppsn) == 9 and ppsn.isdigit():
            break
        print("PPSN must be exactly 9 digits.")
    position = input("Position: ")
    department = input("Department: ")
    available_assets = show_available_assets()
    print("\nEnter asset IDs to assign from the available list above.")
    assets_str = input("Asset IDs (comma-separated, e.g. 11,12): ").strip()
    asset_ids = []
    if assets_str:
        for part in assets_str.split(","):
            part = part.strip()
            if part.isdigit():
                asset_ids.append(int(part))
    data = {
        "name": name,
        "doj": doj_date.isoformat(),
        "address": address,
        "ppsn": ppsn,
        "position": position,
        "department": department,
        "asset_ids": asset_ids
    }
    try:
        r = requests.post(f"{BASE_URL}/onboard", json=data, headers=get_headers())
    except Exception as e:
        print("Error connecting to server:", e)
        return
    if r.status_code not in (200, 201):
        print("Failed to onboard employee.")
        return
    body = r.json()
    print("\nEmployee onboarded successfully.")
    emp = body.get("employee", {})
    assigned = body.get("assigned_assets", [])
    print("\nNew Employee Details:")
    print(f"Employee ID : {emp.get('employee_id')}")
    print(f"Name        : {emp.get('name')}")
    print(f"Department  : {emp.get('department')}")
    print(f"Position    : {emp.get('position')}")
    print(f"DOJ         : {emp.get('doj')}")
    print(f"Address     : {emp.get('address')}")
    print(f"PPSN        : {emp.get('ppsn')}")
    print(f"Status      : {emp.get('status')}")
    print("\nAssigned Assets:")
    if not assigned:
        print("None")
    else:
        for a in assigned:
            print(
                f"ID: {a.get('asset_id')} | "
                f"Name: {a.get('asset_name')} | "
                f"Type: {a.get('asset_type')}"
            )

def offboard_employee():
    if not ensure_logged_in():
        return
    print("\n=== Current Employees ===")
    employees = fetch_employees()
    if employees is None:
        return
    if not employees:
        print("No employees found.")
        return
    for e in employees:
        print(
            f"ID: {e.get('employee_id')} | "
            f"Name: {e.get('name')} | "
            f"Dept: {e.get('department')} | "
            f"Status: {e.get('status')}"
        )
    print("\n=== Offboard Employee ===")
    employee_id = input("Enter Employee ID to offboard (e.g. 2000-001): ").strip()
    if not employee_id:
        print("Employee ID is required.")
        return
    data = {"employee_id": employee_id}
    try:
        r = requests.post(f"{BASE_URL}/offboard", json=data, headers=get_headers())
    except Exception as e:
        print("Error connecting to server:", e)
        return
    if r.status_code != 200:
        print("Failed to offboard employee.")
        return
    body = r.json()
    print("\nEmployee offboarded successfully.")
    emp = body.get("employee", {})
    released = body.get("released_assets", [])
    print("\nOffboarded Employee Details:")
    print(f"Employee ID : {emp.get('employee_id')}")
    print(f"Name        : {emp.get('name')}")
    print(f"Department  : {emp.get('department')}")
    print(f"Position    : {emp.get('position')}")
    print(f"DOJ         : {emp.get('doj')}")
    print(f"Address     : {emp.get('address')}")
    print(f"PPSN        : {emp.get('ppsn')}")
    print(f"Status      : {emp.get('status')}")
    print("\nReleased Assets:")
    if not released:
        print("None")
    else:
        for a in released:
            print(
                f"ID: {a.get('asset_id')} | "
                f"Name: {a.get('asset_name')} | "
                f"Type: {a.get('asset_type')}"
            )

def list_employees():
    if not ensure_logged_in():
        return
    print("\n=== Employees ===")
    employees = fetch_employees()
    if employees is None:
        return
    if not employees:
        print("No employees found.")
        return
    for e in employees:
        print(
            f"ID: {e.get('employee_id')} | "
            f"Name: {e.get('name')} | "
            f"Dept: {e.get('department')} | "
            f"Pos: {e.get('position')} | "
            f"DOJ: {e.get('doj')} | "
            f"Status: {e.get('status')}"
        )

def list_assets():
    if not ensure_logged_in():
        return
    print("\n=== Assets ===")
    assets = fetch_assets()
    if assets is None:
        return
    if not assets:
        print("No assets found.")
        return
    for a in assets:
        assigned_to_id = a.get("assigned_to_id")
        assigned_to_name = a.get("assigned_to_name")
        if assigned_to_id and assigned_to_name:
            assigned_str = f"{assigned_to_id} ({assigned_to_name})"
        elif assigned_to_id:
            assigned_str = assigned_to_id
        else:
            assigned_str = "None"
        print(
            f"ID: {a.get('asset_id')} | "
            f"Name: {a.get('asset_name')} | "
            f"Type: {a.get('asset_type')} | "
            f"Status: {a.get('status')} | "
            f"Assigned to: {assigned_str}"
        )

def view_monthly_report():
    if not ensure_logged_in():
        return
    print("\n=== Monthly HR Report ===")
    year_str = input("Year (YYYY, Enter for current year): ").strip()
    month_str = input("Month (1-12, Enter for current month): ").strip()
    today = date.today()
    if not year_str:
        year_str = str(today.year)
    if not month_str:
        month_str = str(today.month)
    if not year_str.isdigit() or not month_str.isdigit():
        print("Year and month must be numbers.")
        return
    params = {"year": int(year_str), "month": int(month_str)}
    try:
        r = requests.get(f"{BASE_URL}/report/monthly", params=params, headers=get_headers())
    except Exception as e:
        print("Error connecting to server:", e)
        return
    if r.status_code != 200:
        print("Failed to get report:", r.status_code, r.text)
        return
    report = r.json()
    print(f"\nReport for {report.get('month')}/{report.get('year')}")
    print(f"Onboarded: {report.get('onboarded_count', 0)}")
    print(f"Offboarded: {report.get('offboarded_count', 0)}")
    print("\nBy Department:")
    by_dept = report.get("by_department", [])
    if not by_dept:
        print("No data.")
    else:
        for row in by_dept:
            print(
                f"{row.get('department')}: "
                f"Onboarded={row.get('onboarded', 0)}, "
                f"Offboarded={row.get('offboarded', 0)}"
            )

def main_menu():
    while True:
        if auth_token is None:
            print("\n=== Client ===")
            print("1. Login")
            print("0. Exit")
            choice = input("Enter choice: ").strip()
            if choice == "1":
                login()
            elif choice == "0":
                print("Thanks!")
                break
            else:
                print("Invalid choice.")
        else:
            print("\n===  Menu ===")
            print("1. Onboard new employee")
            print("2. Offboard employee")
            print("3. List employees")
            print("4. List assets")
            print("5. View monthly report")
            print("0. Exit")
            choice = input("Enter choice: ").strip()
            if choice == "1":
                onboard_employee()
            elif choice == "2":
                offboard_employee()
            elif choice == "3":
                list_employees()
            elif choice == "4":
                list_assets()
            elif choice == "5":
                view_monthly_report()
            elif choice == "0":
                print("Bye!")
                break
            else:
                print("Invalid")

if __name__ == "__main__":
    main_menu()
