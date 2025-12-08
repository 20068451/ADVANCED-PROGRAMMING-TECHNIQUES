import requests
from bs4 import BeautifulSoup

print("HOTEL SCRAPING SYSTEM")

hotels = [
    ("https://hotel1.tiiny.site", "Hotel 1"),
    ("https://booking-hotels2.tiiny.site/", "Booking Hotels 2")
]

all_rooms = []

print("\nTesting Website Connection...")

for url, name in hotels:
    print(f"\nConnecting to: {name} ({url})")
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            print(f"Connection successful! Status: {response.status_code}")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            page_text = soup.get_text()
            
            print(f"Page text length: {len(page_text)} characters")
            
            lines = page_text.split('\n')
            
            print(f"Found {len(lines)} lines of text")
            
            rooms_found = 0
            
            for i, line in enumerate(lines):
                line = line.strip()
                
                if line and len(line) > 3:
                    print(f"  Line {i+1}: {line[:40]}...")
                    rooms_found += 1
                    
                    if rooms_found >= 3:
                        break
            
            print(f"Total extractable items: {rooms_found}")
            
        else:
            print(f"Connection failed! Status: {response.status_code}")
    
    except Exception as e:
        print(f"Error connecting to {name}: {e}")

print("Website connection tested successfully")