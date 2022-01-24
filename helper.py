import gspread
import pandas as pd


class Sheets:
    """This class will enable saving and retrieving of data from google spreadsheets
    It always retrieves and writes data from and to the given spreadsheet"""

    def __init__(self, sheet_name):
        self.sheet_name = sheet_name
        gc = gspread.service_account()
        self.sheet = gc.open(self.sheet_name).sheet1
        self.df = pd.DataFrame(self.sheet.get_all_records())

    def get_df(self):
        return self.df

    def write_df(self, df):
        self.sheet.update([df.columns.values.tolist()] + df.values.tolist())
        print("log: files successfully written to google sheet")
        return