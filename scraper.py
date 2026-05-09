import requests
from bs4 import BeautifulSoup
import json
import urllib3
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 1. Initialize the list with a "Last Checked" entry for CtrlEnvi
updates = [{
    "title": f"System Live: Last Checked on {datetime.now().strftime('%d %b %Y')}",
    "link": "https://ctrlenvi.com",
    "date": "Today"
}]

portals = {
    "Plastic": "https://eprplastic.cpcb.gov.in/",
    "Battery": "https://eprbattery.cpcb.gov.in/",
    "E-waste": "https://eprewaste.cpcb.gov.in/"
}

headers = {'User-Agent': 'Mozilla/5.0'}

for name, url in portals.items():
    try:
        r = requests.get(url, headers=headers, verify=False, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Look for ANY link that contains common EPR keywords
        all_links = soup.find_all('a')
        for link in all_links:
            text = link.get_text().strip()
            href = link.get('href', '')
            
            # Keywords to look for
            keywords = ["Notice", "Guideline", "Registration", "Portal", "EPR", "Extension", "Public"]
            if any(key.lower() in text.lower() for key in keywords):
                if len(text) > 15: # Ensure it's a real headline
                    updates.append({
                        "title": f"[{name}] {text[:80]}...",
                        "link": href if href.startswith('http') else url + href,
                        "date": "NEW"
                    })
    except Exception as e:
        print(f"Skipping {name} due to connection.")

# Save the file
with open('epr-data.json', 'w') as f:
    json.dump(updates, f, indent=4)
