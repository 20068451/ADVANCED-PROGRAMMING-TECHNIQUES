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

    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Contact Book App");
            bool exit = false;

            while (!exit)
            {
                ShowMenu();
                Console.Write("Enter choice: ");
                string choice = Console.ReadLine();

                switch (choice)
                {
                    case "1":
                        Console.WriteLine("Add Contact");
                        break;
                    case "2":
                        Console.WriteLine("Show All Contacts");
                        break;
                    case "3":
                        Console.WriteLine("Show Contact Details");
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
    }
}