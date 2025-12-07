using System;
using System.Collections.Generic;

namespace FileExtensionInfoApp
{
    public class ExtensionInfoSystem
    {
        private Dictionary<string, string> extensionInfo =
            new Dictionary<string, string>();

        public ExtensionInfoSystem()
        {
            LoadExtensions();
        }

        private void LoadExtensions()
        {
            extensionInfo[".mp4"] = "MP4 video file";
            extensionInfo[".avi"] = "AVI video file";
            extensionInfo[".mov"] = "MOV video file";
            extensionInfo[".mkv"] = "MKV video file";
            extensionInfo[".webm"] = "WEBM video file";
            extensionInfo[".mp3"] = "MP3 audio file";
            extensionInfo[".wav"] = "WAV audio file";
            extensionInfo[".flac"] = "FLAC audio file";
            extensionInfo[".jpg"] = "JPEG image file";
            extensionInfo[".jpeg"] = "JPEG image file";
            extensionInfo[".png"] = "PNG image file";
            extensionInfo[".gif"] = "GIF image file";
            extensionInfo[".pdf"] = "PDF document";
            extensionInfo[".docx"] = "Microsoft Word document";
            extensionInfo[".xlsx"] = "Microsoft Excel spreadsheet";
            extensionInfo[".pptx"] = "Microsoft PowerPoint presentation";
            extensionInfo[".txt"] = "Plain text file";
            extensionInfo[".zip"] = "ZIP archive";
            extensionInfo[".rar"] = "RAR archive";
            extensionInfo[".cs"] = "C# source code file";
            extensionInfo[".html"] = "HTML web page file";
        }

        private string NormalizeExtension(string input)
        {
            if (string.IsNullOrWhiteSpace(input))
            {
                return "";
            }

            string ext = input.Trim().ToLower();

            if (!ext.StartsWith("."))
            {
                ext = "." + ext;
            }

            return ext;
        }

        public void ShowExtensionInfo(string userInput)
        {
            string ext = NormalizeExtension(userInput);

            if (ext == "")
            {
                Console.WriteLine("Enter any extension.");
                return;
            }

            if (extensionInfo.ContainsKey(ext))
            {
                Console.WriteLine("Extension: " + ext);
                Console.WriteLine("Description: " + extensionInfo[ext]);
            }
            else
            {
                Console.WriteLine("Sorry, No information about '" + userInput + "'.");
                Console.WriteLine("Try another extension.");
            }
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            ExtensionInfoSystem system = new ExtensionInfoSystem();
            bool exit = false;

            Console.WriteLine("File Extension Info System");

            while (!exit)
            {
                Console.WriteLine("\nFile Extension Info System");
                Console.WriteLine("1: Look up a file extension");
                Console.WriteLine("0: Exit");
                Console.Write("Enter choice: ");
                
                string choice = Console.ReadLine();

                switch (choice)
                {
                    case "1":
                        Console.Write("Enter file extension (e.g. .mp4 or mp4): ");
                        string input = Console.ReadLine();
                        system.ShowExtensionInfo(input);
                        break;
                    case "0":
                        exit = true;
                        break;
                    default:
                        Console.WriteLine("Invalid");
                        break;
                }
            }

            Console.WriteLine("Thanks!");
        }
    }
}