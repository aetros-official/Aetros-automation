import sys
import os
import sqlite3
import datetime
from modules.web_scraper import WebScraperModule
from modules.data_processor import DataProcessorModule
from modules.data_exporter import DataExporterModule
from modules.scheduler import SchedulerModule
from core.local_db import LocalDBConnector

class AetrosCLIDashboard:
    """Interactive Control Dashboard for managing Aetros Automation Platform."""

    def display_header(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("==========================================================")
        print("          🚀 AETROS AUTOMATION PLATFORM DASHBOARD         ")
        print("==========================================================")
        print("  Status: Active | Engine: Multi-threaded | DB: SQLite & Sheets")
        print("----------------------------------------------------------\n")

    def show_db_stats(self):
        """Fetches quick record stats from the local SQLite DB."""
        db = LocalDBConnector()
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM scraped_backup")
                total_records = cursor.fetchone()[0]
                cursor.execute("SELECT COUNT(DISTINCT url) FROM scraped_backup")
                unique_urls = cursor.fetchone()[0]
                print(f"📊 [Local DB Stats] Total Records: {total_records} | Unique URLs: {unique_urls}")
        except Exception as e:
            print(f"⚠️ [Local DB Stats] Error fetching database summary: {str(e)}")

    def run_instant_workflow(self):
        """Triggers a single-run full automation pipeline immediately."""
        self.display_header()
        print("► Running Instant Full Automation Pipeline...\n")
        from main import full_aetros_workflow
        full_aetros_workflow()
        input("\nPress Enter to return to Main Menu...")

    def run_scheduled_jobs(self):
        """Starts the automated interval scheduler."""
        self.display_header()
        print("► Starting Automated Scheduler...")
        try:
            interval = int(input("Enter schedule interval in seconds (default 10): ") or "10")
            max_runs = int(input("Enter maximum execution runs (default 2): ") or "2")
        except ValueError:
            interval = 10
            max_runs = 2

        from main import full_aetros_workflow
        scheduler = SchedulerModule()
        scheduler.run_interval_job(full_aetros_workflow, interval_seconds=interval, max_runs=max_runs)
        input("\nPress Enter to return to Main Menu...")

    def trigger_data_cleaning(self):
        """Triggers data deduplication and whitespace normalization."""
        self.display_header()
        print("► Executing Data Processor & Deduplication...\n")
        processor = DataProcessorModule()
        processor.run_full_pipeline("Scraped_Data")
        input("\nPress Enter to return to Main Menu...")

    def trigger_data_export(self):
        """Exports dataset to local JSON and CSV files."""
        self.display_header()
        print("► Generating Export Reports (CSV/JSON)...\n")
        exporter = DataExporterModule()
        exporter.export_all("Scraped_Data")
        input("\nPress Enter to return to Main Menu...")

    def main_menu(self):
        """Displays the interactive CLI menu options."""
        while True:
            self.display_header()
            self.show_db_stats()
            print("\n---------------- MENU OPTIONS ----------------")
            print("  1. Run Instant Pipeline (Scrape -> Clean -> Export)")
            print("  2. Start Automated Scheduler (Interval Runs)")
            print("  3. Run Data Processor & Clean Duplicates")
            print("  4. Generate CSV & JSON Local Reports")
            print("  5. Exit Platform Dashboard")
            print("----------------------------------------------")

            choice = input("\nSelect an option (1-5): ").strip()

            if choice == "1":
                self.run_instant_workflow()
            elif choice == "2":
                self.run_scheduled_jobs()
            elif choice == "3":
                self.trigger_data_cleaning()
            elif choice == "4":
                self.trigger_data_export()
            elif choice == "5":
                print("\nExiting Aetros Platform. Goodbye!")
                sys.exit(0)
            else:
                input("\nInvalid option selected. Press Enter to try again...")

if __name__ == "__main__":
    dashboard = AetrosCLIDashboard()
    dashboard.main_menu()
