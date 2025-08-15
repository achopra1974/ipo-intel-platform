import requests
import yaml

with open("config.yaml") as f:
    cfg = yaml.safe_load(f)["nse_api"]

def fetch_listing_status(code: str) -> dict:
    url = cfg["listing_endpoint"]
    headers = cfg["headers"]
    params = {"symbol": code}
    r = requests.get(url, headers=headers, params=params)
    data = r.json()
    # Adapt parsing to actual endpoint response
    return {
        "listing_date": data.get("listingDate"),
        "open": data.get("openPrice"),
        "close": data.get("closePrice"),
    }