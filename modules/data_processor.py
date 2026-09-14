import datetime
import core.db_connector as db_conn
import modules.logger_module as log_mod

class DataProcessorModule:
    """High-performance module for cleaning, filtering, and deduplicating scraped data."""
   
    def __init__(self):
        self.db = None
        for class_name in ['AetrosDB', 'SheetConnector', 'GoogleSheetConnector', 'DBConnector']:
            if hasattr(db_conn, class_name):
                try:
                    cls = getattr(db_conn, class_name)
                    self.db = cls()
                    print(f"[DataProcessor] Connected to DB via: {class_name}")
                    break
                except Exception as e:
                    print(f"[DataProcessor DB Error]: {str(e)}")

        self.logger = None
        for class_name in ['SystemLogger', 'LoggerModule', 'Logger']:
            if hasattr(log_mod, class_name):
                try:
                    cls = getattr(log_mod, class_name)
                    self.logger = cls()
                    break
                except Exception:
                    pass

    def get_worksheet_obj(self, target_worksheet="Scraped_Data"):
        """Utility method to safely fetch the target worksheet."""
        if not self.db:
            print("[DataProcessor Error] Database connection unavailable.")
            return None

        sheet_obj = getattr(self.db, 'sheet', None) or getattr(self.db, 'spreadsheet', None)
        if not sheet_obj:
            print("[DataProcessor Error] Unable to access spreadsheet object.")
            return None

        try:
            return sheet_obj.worksheet(target_worksheet)
        except Exception as e:
            print(f"[DataProcessor Error] Worksheet '{target_worksheet}' not found: {str(e)}")
            return None

    def remove_duplicates_and_clean(self, target_worksheet="Scraped_Data"):
        """Deduplicates records in memory and rewrites clean dataset to minimize API calls."""
        worksheet = self.get_worksheet_obj(target_worksheet)
        if not worksheet:
            return 0

        try:
            all_values = worksheet.get_all_values()
            if not all_values or len(all_values) <= 1:
                print("[DataProcessor Info] No records to process.")
                return 0

            header = all_values[0]
            rows = all_values[1:]

            seen_urls = set()
            clean_rows = []
            removed_count = 0

            for row in rows:
                if len(row) < 2:
                    continue
                url = row[1].strip()
               
                # Title whitespace normalization
                if len(row) >= 3:
                    row[2] = " ".join(str(row[2]).split())

                if url and url not in seen_urls:
                    seen_urls.add(url)
                    clean_rows.append(row)
                else:
                    removed_count += 1

            if removed_count > 0:
                worksheet.clear()
                worksheet.append_row(header)
                if clean_rows:
                    worksheet.append_rows(clean_rows)
                print(f"[DataProcessor Success] Cleaned dataset. Removed {removed_count} duplicate records.")
            else:
                print("[DataProcessor Success] No duplicates found. Dataset is clean.")

            return removed_count

        except Exception as e:
            print(f"[DataProcessor Error] Failed to process records: {str(e)}")
            return 0

    def run_full_pipeline(self, target_worksheet="Scraped_Data"):
        """Runs optimization pipeline."""
        print(f"\n--- Running Optimized Data Pipeline on '{target_worksheet}' ---")
        removed_dupes = self.remove_duplicates_and_clean(target_worksheet)
        print("--- Data Pipeline Complete ---\n")
        return {"removed_duplicates": removed_dupes}
