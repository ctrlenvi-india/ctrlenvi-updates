# ctrlenvi-updates
import requests
from bs4 import BeautifulSoup
import datetime

# The list of CPCB portals you want to watch
portals = {
    "Plastic": "https://eprplastic.cpcb.gov.in/",
    "Battery": "https://eprbattery.cpcb.gov.in/",
    "E-Waste": "https://eprewaste.cpcb.gov.in/"
}

def scrape_cpcb():
    for name, url in portals.items():
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # This looks for 'marquee' tags where gov sites put news
            news_items = soup.find_all('marquee')
            
            for item in news_items:
                print(f"[{name}] {datetime.date.today()}: {item.text.strip()}")
        except Exception as e:
            print(f"Error checking {name}: {e}")

if _name_ == "_main_":
    scrape_cpcb()