import gspread
from oauth2client.service_account import ServiceAccountCredentials
import yaml

with open("config.yaml") as f:
    cfg = yaml.safe_load(f)["google_sheets"]

def init_sheet():
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        cfg["creds_file"], scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(cfg["sheet_key"]).sheet1
    return sheet

def append_rows(rows):
    sheet = init_sheet()
    for row in rows:
        sheet.append_row(row)