import requests
from bs4 import BeautifulSoup
import yaml

with open("config.yaml") as f:
    cfg = yaml.safe_load(f)["scraper"]

def scrape_sebi():
    url = next(s["url"] for s in cfg["sources"] if "sebi.gov.in" in s["url"])
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    # Example: locate table rows
    rows = soup.select("table tr")[1:]
    ipos = []
    for tr in rows:
        cols = [td.text.strip() for td in tr.find_all("td")]
        ipos.append({
            "code": cols[0],
            "name": cols[1],
            "open_date": cols[2],
            "close_date": cols[3],
            "lot_size": int(cols[4]),
            "price_range": cols[5],
            "min_invest": float(cols[4]) * float(cols[5].split("-")[0]),
            "current_gmp": None,
            "allotment_date": cols[6],
            "refund_date": cols[7],
            "listing_date": cols[8],
        })
    return ipos

def scrape_chittorgarh():
    url = next(s["url"] for s in cfg["sources"] if "chittorgarh.com" in s["url"])
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")
    # Parse accordingly; placeholder logic below
    ipos = []
    for tr in soup.select(".ipo-table tr")[1:]:
        cols = [td.text.strip() for td in tr.find_all("td")]
        ipos.append({
            "code": cols[0],
            "name": cols[1],
            "open_date": cols[2],
            "close_date": cols[3],
            "lot_size": int(cols[4]),
            "price_range": cols[5],
            "min_invest": int(cols[4]) * float(cols[5].split("-")[0]),
            "current_gmp": float(cols[6].replace("+","")) if cols[6] else None,
            "allotment_date": cols[7],
            "refund_date": cols[8],
            "listing_date": cols[9],
        })
    return ipos

def scrape_all():
    return scrape_sebi() + scrape_chittorgarh()