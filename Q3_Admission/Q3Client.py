import socket
import json

HOST = "127.0.0.1"
PORT = 5000

def get_name():
    name = input("Full Name: ").strip()
    return name

def get_address():
    address = input("Address: ").strip()
    return address

def get_qualifications():
    qualifications = input("Educational Qualifications: ").strip()
    return qualifications

def choose_course():
    print("Choose Courses:")
    print("1. MSc in Cyber Security")
    print("2. MSc Information Systems & Computing")
    print("3. MSc Data Analytics")
    
    while True:
        choice = input("Enter 1, 2, or 3: ").strip()
        if choice == "1":
            return "MSc in Cyber Security"
        elif choice == "2":
            return "MSc Information Systems & Computing"
        elif choice == "3":
            return "MSc Data Analytics"
        else:
            print("Invalid")

def get_start_year():
    while True:
        year = input("Start Year: ").strip()
        if year.isdigit():
            return int(year)
        print("Enter number")

def get_start_month():
    while True:
        month = input("Start Month: ").strip()
        if month.isdigit():
            return int(month)
        print("Enter number")

def send_application(app_data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    
    json_data = json.dumps(app_data)
    sock.send(json_data.encode('utf-8'))
    
    response = sock.recv(4096).decode('utf-8')
    result = json.loads(response)
    
    sock.close()
    
    return result

def main():
    print("DBS Admission")
    
    name = get_name()
    address = get_address()
    qualifications = get_qualifications()
    course = choose_course()
    start_year = get_start_year()
    start_month = get_start_month()
    
    app_data = {
        "name": name,
        "address": address,
        "qualifications": qualifications,
        "course": course,
        "start_year": start_year,
        "start_month": start_month
    }
    
    print("\nSending to server...")
    
    try:
        result = send_application(app_data)
        
        if result["status"] == "ok":
            print(f"\nApplication Successful!")
            print(f"Registration Number: {result['registration_number']}")
        else:
            print("\nApplication Failed")
    
    except ConnectionRefusedError:
        print("\nCannot connect to server")
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    main()