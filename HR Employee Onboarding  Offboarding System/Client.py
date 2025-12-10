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
    except Exception as e:
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
    except:
        msg = "Invalid username or password"

    print("Login failed:", msg)
    return False


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
            print("\nYou are logged in.")
            print("0. Exit")
            choice = input("Enter choice: ").strip()

            if choice == "0":
                print("Thanks!")
                break
            else:
                print("Invalid choice.")


if __name__ == "__main__":
    main_menu()
