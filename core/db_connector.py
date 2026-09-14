import os
import gspread

class AetrosDB:
    def __init__(self, sheet_name="Aetros Database"):
        # Find root folder path dynamically
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
       
        # Check credentials in config/ folder or root directory
        config_path = os.path.join(base_dir, "config", "google_credentials.json")
        root_path = os.path.join(base_dir, "google_credentials.json")
       
        if os.path.exists(config_path):
            self.cred_path = config_path
        elif os.path.exists(root_path):
            self.cred_path = root_path
        else:
            raise FileNotFoundError("google_credentials.json not found in root or config/ directory.")
       
        # Authenticate and open Google Spreadsheet
        self.gc = gspread.service_account(filename=self.cred_path)
        self.spreadsheet = self.gc.open(sheet_name)

    def get_worksheet(self, title):
        return self.spreadsheet.worksheet(title)

    def append_row(self, worksheet_name, row_data):
        sheet = self.get_worksheet(worksheet_name)
        sheet.append_row(row_data)
