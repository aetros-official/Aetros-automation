import gspread

try:
    # Authenticate via Service Account
    gc = gspread.service_account(filename="google_credentials.json")
   
    # Open the spreadsheet
    sh = gc.open("Aetros Database")
    worksheet = sh.sheet1
   
    # Write test data
    worksheet.update_acell("A1", "Aetros Status")
    worksheet.update_acell("B1", "Connected Successfully!")
   
    print("\nSUCCESS: Connected to Google Sheets successfully!\n")

except Exception as e:
    print(f"\nERROR: Connection failed:\n{e}")