import requests
from bs4 import BeautifulSoup
import csv
import os

print("HOTEL SCRAPING SYSTEM")
print("-" * 40)

hotels = [
    ("https://hotel1.tiiny.site", "Hotel 1"),
    ("https://booking-hotels2.tiiny.site/", "Booking Hotels 2")
]

all_rooms = []
SEASON_PERIOD = "20-30 December"

print("\nScraping websites for room prices...\n")

for url, name in hotels:
    print(f"Connecting to: {name} ({url})")

    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            print(f"  Connection OK (status {response.status_code})")

            soup = BeautifulSoup(response.text, "html.parser")
            page_text = soup.get_text(separator="\n")
            lines = page_text.split("\n")

            rooms_found_for_this_hotel = 0
            seen_lines = set()

            for line in lines:
                line = line.strip()

                if "€" in line and len(line) > 3:
                    if line in seen_lines:
                        continue
                    seen_lines.add(line)

                    rooms_found_for_this_hotel += 1

                    all_rooms.append({
                        "hotel_name": name,
                        "source_url": url,
                        "season_period": SEASON_PERIOD,
                        "room_description": line
                    })

            print(f"  Rooms found on this website: {rooms_found_for_this_hotel}\n")
        else:
            print(f"  Connection failed (status {response.status_code})\n")

    except Exception as e:
        print(f"  Error while connecting to {name}: {e}\n")

print("-" * 40)
print(f"Total rooms collected from all hotels: {len(all_rooms)}")
print("-" * 40)

csv_filename = "hotel_prices.csv"
csv_path = os.path.join(os.getcwd(), csv_filename)

fieldnames = ["hotel_name", "source_url", "season_period", "room_description"]

with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    if all_rooms:
        writer.writerows(all_rooms)

print(f"\nCSV file created at:\n  {csv_path}")

print("\nData from CSV and Displaying:\n")

try:
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

        if not rows:
            print("CSV is empty.")
        else:
            for i, row in enumerate(rows, start=1):
                print(f"Room #{i}")
                print(f"  Hotel:   {row['hotel_name']}")
                print(f"  URL:     {row['source_url']}")
                print(f"  Season:  {row['season_period']}")
                print(f"  Details: {row['room_description']}")
                print("-" * 40)

except FileNotFoundError:
    print("CSV not found.")
