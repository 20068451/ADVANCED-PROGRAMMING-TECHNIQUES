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

def main():
    print("DBS Admission")
    
    name = get_name()
    address = get_address()
    qualifications = get_qualifications()
    course = choose_course()
    start_year = get_start_year()
    start_month = get_start_month()
    
    print("\nApplication Data:")
    print(f"Name: {name}")
    print(f"Address: {address}")
    print(f"Qualifications: {qualifications}")
    print(f"Course: {course}")
    print(f"Start: {start_month}/{start_year}")

if __name__ == "__main__":
    main()