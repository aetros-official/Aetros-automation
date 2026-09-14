import os
import gspread

# Find the file directory path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_PATH = os.path.join(BASE_DIR, "google_credentials.json")

def initialize_aetros_db():
    try:
        # Google Sheets Service Account Connection
        gc = gspread.service_account(filename=CREDENTIALS_PATH)
        sh = gc.open("Aetros Database")

        # 1. Logs Sheet
        try:
            logs_sheet = sh.worksheet("Logs")
        except gspread.exceptions.WorksheetNotFound:
            logs_sheet = sh.add_worksheet(title="Logs", rows="100", cols="20")
       
        logs_sheet.update("A1:C1", [["Timestamp", "Event Level", "Message"]])

        # 2. Workflows Sheet
        try:
            wf_sheet = sh.worksheet("Workflows")
        except gspread.exceptions.WorksheetNotFound:
            wf_sheet = sh.add_worksheet(title="Workflows", rows="100", cols="20")
           
        wf_sheet.update("A1:D1", [["Task ID", "Task Name", "Status", "Last Run"]])

        # Rename default Sheet1
        main_sheet = sh.sheet1
        main_sheet.update_title("Overview")

        print("\n✅ Aetros Database Schema initialized successfully!\n")

    except Exception as e:
        print(f"\n❌ Failed to setup database structure:\n{e}")

if __name__ == "__main__":
    initialize_aetros_db()
