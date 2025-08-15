import sqlite3
from typing import List, Dict

DB_FILE = "ipos.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS ipo (
        code TEXT PRIMARY KEY,
        name TEXT,
        open_date TEXT,
        close_date TEXT,
        lot_size INTEGER,
        price_range TEXT,
        min_invest REAL,
        current_gmp REAL,
        allotment_date TEXT,
        refund_date TEXT,
        listing_date TEXT,
        last_updated TEXT
    )""")
    conn.commit()
    conn.close()

def upsert_ipos(ipos: List[Dict]):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    for ipo in ipos:
        c.execute("""
        INSERT INTO ipo(code,name,open_date,close_date,lot_size,
            price_range,min_invest,current_gmp,allotment_date,refund_date,
            listing_date,last_updated)
        VALUES(:code,:name,:open_date,:close_date,:lot_size,
               :price_range,:min_invest,:current_gmp,:allotment_date,
               :refund_date,:listing_date,datetime('now'))
        ON CONFLICT(code) DO UPDATE SET
            open_date=excluded.open_date,
            close_date=excluded.close_date,
            lot_size=excluded.lot_size,
            price_range=excluded.price_range,
            min_invest=excluded.min_invest,
            current_gmp=excluded.current_gmp,
            allotment_date=excluded.allotment_date,
            refund_date=excluded.refund_date,
            listing_date=excluded.listing_date,
            last_updated=datetime('now')
        """, ipo)
    conn.commit()
    conn.close()

def fetch_all():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM ipo ORDER BY open_date")
    rows = c.fetchall()
    conn.close()
    return rows