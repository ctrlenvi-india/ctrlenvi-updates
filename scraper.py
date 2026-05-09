import requests
from bs4 import BeautifulSoup
import json
import urllib3

# This helps ignore SSL errors if the CPCB site is being difficult
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

updates = []

portals = {
    "Plastic": "https://eprplastic.cpcb.gov.in/",
    "Battery": "https://eprbattery.cpcb.gov.in/",
    "E-waste": "https://eprewaste.cpcb.gov.in/"
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

for name, url in portals.items():
    try:
        response = requests.get(url, headers=headers, verify=False, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for links inside 'marquee' tags or 'news' sections
        links = soup.find_all('a')
        
        for link in links:
            text = link.get_text().strip()
            href = link.get('href', '#')
            
            # This looks for anything related to notices or new guidelines
            if len(text) > 10: # Avoid tiny buttons or single words
                updates.append({
                    "title": f"[{name}] {text}",
                    "link": href if href.startswith('http') else url + href,
                    "date": "Latest"
                })
    except Exception as e:
        print(f"Error on {name}: {e}")

# Save the results (Only if we found something, to avoid empty [] )
if not updates:
    updates.append({"title": "Check CPCB Portal for latest guidelines", "link": "https://cpcb.nic.in/", "date": "Live"})

with open('epr-data.json', 'w') as f:
    json.dump(updates, f, indent=4)
