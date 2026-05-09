import requests
from bs4 import BeautifulSoup
import datetime
# This line hides the messy warning messages about security
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

portals = {
    "Plastic": "https://eprplastic.cpcb.gov.in/",
    "Battery": "https://eprbattery.cpcb.gov.in/",
    "E-Waste": "https://eprewaste.cpcb.gov.in/"
}

def scrape_cpcb():
    for name, url in portals.items():
        try:
            # We added 'verify=False' to skip the security error
            response = requests.get(url, timeout=15, verify=False)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Looking for the news items
            news_items = soup.find_all('marquee')
            
            if not news_items:
                print(f"[{name}] Connected! But no news found on the marquee.")
            
            for item in news_items:
                print(f"[{name}] {datetime.date.today()}: {item.text.strip()}")
                
        except Exception as e:
            print(f"Error checking {name}: {e}")

if __name__ == "__main__":
    scrape_cpcb()
    import json
import subprocess

# ... (your existing scraping logic) ...

# 1. Save the data to the file
with open('epr-data.json', 'w') as f:
    json.dump(updates, f, indent=4)

# 2. Tell the Bot to push this file back to your repo
try:
    subprocess.run(["git", "config", "user.name", "scraper-bot"], check=True)
    subprocess.run(["git", "config", "user.email", "bot@ctrlenvi.com"], check=True)
    subprocess.run(["git", "add", "epr-data.json"], check=True)
    subprocess.run(["git", "commit", "-m", "Auto-update EPR data"], check=True)
    subprocess.run(["git", "push"], check=True)
    print("File pushed successfully!")
except Exception as e:
    print(f"Error pushing to Git: {e}")
