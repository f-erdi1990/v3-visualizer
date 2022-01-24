import gspread
import os
import json
import pandas as pd

ON_HEROKU = os.environ.get("ON_HEROKU")
if ON_HEROKU:
    print("log: system is aware its on heroku")
    string_gs_service = os.environ.get('GS_SERVICE')
    GS_SERVICE = json.loads(string_gs_service)
else:
    print("log: system is aware it is not on heroku")
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    GS_TOKEN_PATH = os.path.join(ROOT_DIR, 'gs-token.json')
    try:
        with open(GS_TOKEN_PATH, 'r') as f:
            GS_SERVICE = json.load(f)
    except FileNotFoundError:
        print("log: google sheets token file not found")


class Sheets:
    """This class will enable saving and retrieving of data from google spreadsheets
    It always retrieves and writes data from and to the given spreadsheet"""

    def __init__(self, sheet_name):
        self.sheet_name = sheet_name
        gc = gspread.service_account_from_dict(GS_SERVICE)
        self.sheet = gc.open(self.sheet_name).sheet1
        self.df = pd.DataFrame(self.sheet.get_all_records())

    def get_df(self):
        return self.df

    def write_df(self, df):
        self.sheet.update([df.columns.values.tolist()] + df.values.tolist())
        print("log: files successfully written to google sheet")
        return
