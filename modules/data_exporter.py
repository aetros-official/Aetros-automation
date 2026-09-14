import os
import json
import csv
import datetime
import core.db_connector as db_conn
import modules.logger_module as log_mod

class DataExporterModule:
    """Module responsible for exporting processed Google Sheets data to local CSV and JSON reports."""

    def __init__(self, output_dir="exports"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        self.db = None
        for class_name in ['AetrosDB', 'SheetConnector', 'GoogleSheetConnector', 'DBConnector']:
            if hasattr(db_conn, class_name):
                try:
                    cls = getattr(db_conn, class_name)
                    self.db = cls()
                    print(f"[DataExporter] Connected to DB via: {class_name}")
                    break
                except Exception as e:
                    print(f"[DataExporter DB Error]: {str(e)}")

        self.logger = None
        for class_name in ['SystemLogger', 'LoggerModule', 'Logger']:
            if hasattr(log_mod, class_name):
                try:
                    cls = getattr(log_mod, class_name)
                    self.logger = cls()
                    break
                except Exception:
                    pass

    def fetch_sheet_data(self, target_worksheet="Scraped_Data"):
        """Fetches all records from the target worksheet."""
        if not self.db:
            print("[DataExporter Error] Database connection unavailable.")
            return []

        sheet_obj = getattr(self.db, 'sheet', None) or getattr(self.db, 'spreadsheet', None)
        if not sheet_obj:
            print("[DataExporter Error] Unable to access spreadsheet object.")
            return []

        try:
            worksheet = sheet_obj.worksheet(target_worksheet)
            records = worksheet.get_all_records()
            return records
        except Exception as e:
            print(f"[DataExporter Error] Failed to fetch records: {str(e)}")
            return []

    def export_to_json(self, target_worksheet="Scraped_Data", filename=None):
        """Exports worksheet data into a formatted JSON report file."""
        data = self.fetch_sheet_data(target_worksheet)
        if not data:
            print("[DataExporter Warning] No data available to export to JSON.")
            return None

        if not filename:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"scraped_report_{timestamp}.json"

        file_path = os.path.join(self.output_dir, filename)

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"[DataExporter Success] JSON report generated: {file_path}")
            return file_path
        except Exception as e:
            print(f"[DataExporter Error] Failed to write JSON file: {str(e)}")
            return None

    def export_to_csv(self, target_worksheet="Scraped_Data", filename=None):
        """Exports worksheet data into a clean CSV file."""
        data = self.fetch_sheet_data(target_worksheet)
        if not data:
            print("[DataExporter Warning] No data available to export to CSV.")
            return None

        if not filename:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"scraped_report_{timestamp}.csv"

        file_path = os.path.join(self.output_dir, filename)

        try:
            headers = list(data[0].keys())
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(data)
            print(f"[DataExporter Success] CSV report generated: {file_path}")
            return file_path
        except Exception as e:
            print(f"[DataExporter Error] Failed to write CSV file: {str(e)}")
            return None

    def export_all(self, target_worksheet="Scraped_Data"):
        """Executes both JSON and CSV export processes sequentially."""
        print(f"\n--- Running Data Exporter for '{target_worksheet}' ---")
        json_file = self.export_to_json(target_worksheet)
        csv_file = self.export_to_csv(target_worksheet)
        print("--- Data Export Complete ---\n")
        return {"json": json_file, "csv": csv_file}
