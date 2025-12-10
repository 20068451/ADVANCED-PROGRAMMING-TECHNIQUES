import requests
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
    print("\n=== HR Login===")
    username = input("Username: ")
    password = getpass("Password: ")

    data = {"username": username, "password": password}

    try:
        r = requests.post(f"{BASE_URL}/login", json=data)
    except Exception:
        print("Error connecting to server.")
        return False

    if r.status_code == 200:
        body = r.json()
        token = body.get("token")
        if token:
            auth_token = token
            print("Login successful.")
            return True

    try:
        body = r.json()
        msg = body.get("error", "Invalid username or password")
    except Exception:
        msg = "Invalid username or password"

    print("Login failed:", msg)
    return False

def list_employees():
    print("\n=== Employees ===")
    try:
        r = requests.get(f"{BASE_URL}/employees", headers=get_headers())
    except Exception:
        print("Error connecting to server.")
        return

    if r.status_code != 200:
        print("Failed to fetch employees.")
        return

    data = r.json()
    employees = data.get("employees", [])
    if not employees:
        print("No employees found.")
        return

    for e in employees:
        print(
            f"{e['employee_id']} - {e['name']} "
            f"({e['department']}, {e['position']}) - {e['status']}"
        )

def list_assets():
    print("\n=== Assets ===")
    try:
        r = requests.get(f"{BASE_URL}/assets", headers=get_headers())
    except Exception:
        print("Error connecting to server.")
        return

    if r.status_code != 200:
        print("Failed to fetch assets.")
        return

    data = r.json()
    assets = data.get("assets", [])
    if not assets:
        print("No assets found.")
        return

    for a in assets:
        assigned_str = "Available"
        if a["assigned_to"]:
            if a.get("employee_name"):
                assigned_str = f"Assigned to {a['assigned_to']} ({a['employee_name']})"
            else:
                assigned_str = f"Assigned to {a['assigned_to']}"
        print(
            f"{a['asset_id']}: {a['asset_name']} "
            f"[{a['asset_type']}] - {a['status']} - {assigned_str}"
        )

def main_menu():
    while True:
        if auth_token is None:
            print("\n=== Client===")
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
            print("\n=== HR Menu===")
            print("1. List employees")
            print("2. List assets")
            print("0. Exit")
            choice = input("Enter choice: ").strip()

            if choice == "1":
                list_employees()
            elif choice == "2":
                list_assets()
            elif choice == "0":
                print("Thanks!")
                break
            else:
                print("Invalid choice.")

if __name__ == "__main__":
    main_menu()
