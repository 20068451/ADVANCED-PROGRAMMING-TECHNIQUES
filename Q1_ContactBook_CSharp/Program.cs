using System;
using System.Collections.Generic;

namespace ContactBookApp
{
    public class Contact
    {
        private string firstName;
        private string lastName;
        private string company;
        private string mobileNumber;
        private string email;
        private DateTime birthDate;

        public string FirstName
        {
            get { return firstName; }
            set { firstName = value; }
        }

        public string LastName
        {
            get { return lastName; }
            set { lastName = value; }
        }

        public string Company
        {
            get { return company; }
            set { company = value; }
        }

        public string MobileNumber
        {
            get { return mobileNumber; }
            set { mobileNumber = value; }
        }

        public string Email
        {
            get { return email; }
            set { email = value; }
        }

        public DateTime BirthDate
        {
            get { return birthDate; }
            set { birthDate = value; }
        }

        public Contact(string firstName, string lastName, string company,
                       string mobileNumber, string email, DateTime birthDate)
        {
            FirstName = firstName;
            LastName = lastName;
            Company = company;
            MobileNumber = mobileNumber;
            Email = email;
            BirthDate = birthDate;
        }

        public void ShowDetails()
        {
            Console.WriteLine("First Name : " + FirstName);
            Console.WriteLine("Last Name  : " + LastName);
            Console.WriteLine("Company    : " + Company);
            Console.WriteLine("Mobile No. : " + MobileNumber);
            Console.WriteLine("Email      : " + Email);
            Console.WriteLine("Birthdate  : " + BirthDate.ToShortDateString());
        }

        public string GetSummary()
        {
            return FirstName + " " + LastName + " (" + MobileNumber + ")";
        }
    }

    public class ContactBook
    {
        private List<Contact> contacts = new List<Contact>();
        public ContactBook()
        {
            SampleContacts();
        }
        public void AddContact(Contact contact)
        {
            contacts.Add(contact);
        }
        public void AddContact(string firstName, string lastName, string company,
                               string mobileNumber, string email, DateTime birthDate)
        {
            Contact c = new Contact(firstName, lastName, company, mobileNumber, email, birthDate);
            contacts.Add(c);
        }
        public void ShowAllContacts()
        {
            if (contacts.Count == 0)
            {
                Console.WriteLine("No contacts");
                return;
            }

            Console.WriteLine("----- All Contacts -----");
            for (int i = 0; i < contacts.Count; i++)
            {
                Console.WriteLine((i + 1) + ": " + contacts[i].GetSummary());
            }
        }
                public void ShowContactDetails(int index)
        {
            if (index < 0 || index >= contacts.Count)
            {
                Console.WriteLine("Invalid contact number.");
                return;
            }

            Console.WriteLine("----- Contact Details -----");
            contacts[index].ShowDetails();
        }
                public static bool IsValidMobile(string mobile)
        {
            if (mobile.Length != 9)
                return false;

            foreach (char ch in mobile)
            {
                if (!char.IsDigit(ch))
                    return false;
            }

            if (mobile == "000000000")
                return false;

            return true;
        }
        private void SampleContacts()
        {
            AddContact("Wai", "Aung", "Dublin Business School", "799899361", "waiaung@dbs.ie", new DateTime(1990, 1, 1));
            AddContact("Thukha", "Aung", "ABC", "799899362", "thukhaaung@abc.com", new DateTime(1985, 5, 10));
            AddContact("Tet Tun", "Kyaw", "XYZ Ltd", "799899363", "tettunkyaw@xyz.com", new DateTime(1992, 3, 20));
            AddContact("Zaw Htet", "Aung", "Tech Co", "799899364", "zawhtetaung@tech.com", new DateTime(1988, 7, 15));
            AddContact("Pai", "Pai", "Finance Inc", "799899365", "paipai@fin.com", new DateTime(1991, 9, 30));
            AddContact("Kyaw Thet", "Paing", "Retail Corp", "799899366", "kyawthetpaing@retail.com", new DateTime(1983, 11, 5));
            AddContact("Wai", "Yan", "HealthCare", "799899367", "waiyan@health.com", new DateTime(1994, 4, 18));
            AddContact("Nyi", "Nyi", "Travel Co", "799899368", "nyinyi@travel.com", new DateTime(1987, 8, 8));
            AddContact("Aung", "Aung", "Food Co", "799899369", "aungaung@food.com", new DateTime(1993, 2, 2));
            AddContact("Wai", "Mon", "Media Ltd", "799899370", "waimon@media.com", new DateTime(1989, 6, 6));
            AddContact("Aung Myo", "Min", "Bank", "799899371", "aungmyomin@bank.com", new DateTime(1990, 12, 12));
            AddContact("Nyi Nyi", "Maung", "DBS", "799899372", "nyinyimaung@dbs.ie", new DateTime(1986, 1, 25));
            AddContact("Ko", "Maung", "School", "799899373", "komaung@school.com", new DateTime(1995, 10, 10));
            AddContact("Aung", "Nyi", "Shop", "799899374", "aungnyi@shop.com", new DateTime(1984, 9, 9));
            AddContact("Tin Mg Mg", "Tun", "Gym", "799899375", "tinmgmgtun@gym.com", new DateTime(1992, 11, 11));
            AddContact("Nyi", "Bwar", "Restaurant", "799899376", "nyibwar@rest.com", new DateTime(1987, 3, 3));
            AddContact("Ko", "Ko", "Hotel", "799899377", "koko@hotel.com", new DateTime(1991, 4, 4));
            AddContact("Sein", "Khanig", "Logistics", "799899378", "seinkhanig@logi.com", new DateTime(1985, 5, 5));
            AddContact("Thar", "Thar", "Clinic", "799899379", "tharthar@clinic.com", new DateTime(1993, 6, 6));
            AddContact("Chan", "Chan", "DBS", "799899380", "chanchan@dbs.ie", new DateTime(1988, 7, 7));
        }
    }
    class Program
    {
        static void Main(string[] args)
        {
            ContactBook contactBook = new ContactBook();
            bool exit = false;

            while (!exit)
            {
                ShowMenu();
                Console.Write("Enter choice: ");
                string choice = Console.ReadLine();

                switch (choice)
                {
                    case "1":
                        AddContactUI(contactBook);
                        break;
                    case "2":
                        contactBook.ShowAllContacts();
                        break;
                    case "3":
                        Console.WriteLine("Contact Details");
                        break;
                    case "4":
                        Console.WriteLine("Update Contact");
                        break;
                    case "5":
                        Console.WriteLine("Delete Contact");
                        break;
                    case "0":
                        exit = true;
                        break;
                    default:
                        Console.WriteLine("Invalid");
                        break;
                }

                Console.WriteLine();
            }

            Console.WriteLine("Thanks");
        }

        static void ShowMenu()
        {
            Console.WriteLine("-----------------------------------------");
            Console.WriteLine("Main Menu");
            Console.WriteLine("1: Add Contact");
            Console.WriteLine("2: Show All Contacts");
            Console.WriteLine("3: Show Contact Details");
            Console.WriteLine("4: Update Contact");
            Console.WriteLine("5: Delete Contact");
            Console.WriteLine("0: Exit");
            Console.WriteLine("-----------------------------------------");
        }

        static void AddContactUI(ContactBook contactBook)
        {
            Console.WriteLine("----- Add Contact -----");

            Console.Write("First Name: ");
            string firstName = Console.ReadLine();

            Console.Write("Last Name: ");
            string lastName = Console.ReadLine();

            Console.Write("Company: ");
            string company = Console.ReadLine();

            string mobile;
            while (true)
            {
                Console.Write("Mobile Number (9 digits): ");
                mobile = Console.ReadLine();
                if (ContactBook.IsValidMobile(mobile))
                    break;
                Console.WriteLine("Invalid Mobile Number");
            }

            Console.Write("Email: ");
            string email = Console.ReadLine();

            DateTime birthDate;
            while (true)
            {
                Console.Write("Birthdate (e.g. 12/31/1990): ");
                string inputDate = Console.ReadLine();
                if (DateTime.TryParse(inputDate, out birthDate))
                    break;
                Console.WriteLine("Invalid date. Try again.");
            }

            contactBook.AddContact(firstName, lastName, company, mobile, email, birthDate);
            Console.WriteLine("Contact Added.");
        }
    }
}