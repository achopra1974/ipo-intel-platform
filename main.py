import argparse
from datetime import datetime
from scraper import scrape_all
from nse_api import fetch_listing_status
from db import init_db, upsert_ipos, fetch_all
from sheets import append_rows
from notifier import send_email, send_telegram

def format_ipo(ipo):
    return (
        ipo["code"], ipo["name"], ipo["open_date"], ipo["close_date"],
        ipo["lot_size"], ipo["price_range"], ipo["min_invest"],
        ipo.get("current_gmp"), ipo["allotment_date"],
        ipo["refund_date"], ipo["listing_date"]
    )

def main(init=False):
    init_db()

    # 1. Scrape
    ipos = scrape_all()

    # 2. Enrich with NSE data
    for ipo in ipos:
        status = fetch_listing_status(ipo["code"])
        ipo["listing_date"] = status["listing_date"] or ipo["listing_date"]
        ipo["current_gmp"] = status.get("close") if ipo["current_gmp"] is None else ipo["current_gmp"]

    # 3. Upsert into DB
    upsert_ipos(ipos)

    # 4. Audit trail
    now = datetime.now().isoformat()
    rows = [
        [*format_ipo(ipo), now] for ipo in ipos
    ]
    append_rows(rows)

    # 5. Notify
    body = "\n".join([
        f"{ipo['code']} | Open: {ipo['open_date']} | Close: {ipo['close_date']} | GMP: {ipo['current_gmp']}"
        for ipo in ipos
    ])
    subject = f"IPO Daily Update – {datetime.today().date()}"
    send_email(subject, body)
    send_telegram(body)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--init", action="store_true",
                        help="Initial run to populate DB and sheets")
    args = parser.parse_args()
    main(init=args.init)