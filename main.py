from modules.web_scraper import WebScraperModule
from modules.data_processor import DataProcessorModule
from modules.data_exporter import DataExporterModule
from modules.scheduler import SchedulerModule
from modules.alert_module import AlertModule

# Optional Telegram/Email Setup (Replace with your keys if active)
TELEGRAM_BOT_TOKEN = ""      # Example: "123456789:ABCdef..."
TELEGRAM_CHAT_ID = ""        # Example: "987654321"

SMTP_CONFIG = {
    "sender_email": "",      # Example: "yourname@gmail.com"
    "sender_password": "",   # App Password
    "recipient_email": "",   # Recipient
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587
}

def fetch_target_urls_from_sheet(db_instance):
    """Fetches target URLs dynamically from the 'Targets' worksheet."""
    try:
        sheet_obj = getattr(db_instance, 'sheet', None) or getattr(db_instance, 'spreadsheet', None)
        if sheet_obj:
            try:
                targets_ws = sheet_obj.worksheet("Targets")
                records = targets_ws.get_all_records()
                urls = [str(r.get("URL", "")).strip() for r in records if r.get("URL")]
                if urls:
                    print(f"[Targets] Fetched {len(urls)} target URLs from Google Sheet.")
                    return urls
            except Exception:
                print("[Targets Info] 'Targets' tab not found or empty. Using default targets.")
    except Exception as e:
        print(f"[Targets Error] Could not fetch targets: {str(e)}")

    return [
        "https://en.wikipedia.org/wiki/Main_Page",
        "https://www.python.org",
        "https://httpbin.org/status/200"
    ]

def full_aetros_workflow():
    """Defines the optimized end-to-end execution pipeline with notifications."""
    alert_sys = AlertModule(
        telegram_token=TELEGRAM_BOT_TOKEN,
        telegram_chat_id=TELEGRAM_CHAT_ID,
        smtp_config=SMTP_CONFIG
    )

    try:
        scraper = WebScraperModule(max_workers=5)
        target_urls = fetch_target_urls_from_sheet(scraper.db)
       
        # 1. Multi-threaded Web Scraping
        scraped_results = scraper.scrape_multiple_urls(target_urls)
       
        # 2. In-Memory Clean & Deduplication
        processor = DataProcessorModule()
        proc_stats = processor.run_full_pipeline("Scraped_Data")

        # 3. Export Processed Data
        exporter = DataExporterModule()
        exported_files = exporter.export_all("Scraped_Data")

        # 4. Dispatch System Status Alert
        alert_sys.notify_workflow_status(
            total_scraped=len(scraped_results),
            clean_records=len(scraped_results) - proc_stats.get("removed_duplicates", 0),
            exported_files=exported_files
        )

    except Exception as e:
        print(f"[Workflow Critical Error]: {str(e)}")
        alert_sys.notify_workflow_status(0, 0, None, error_message=str(e))

def main():
    print("=== Aetros High-Performance Platform with Alerting Starting ===\n")
    scheduler = SchedulerModule()
    scheduler.run_interval_job(full_aetros_workflow, interval_seconds=5, max_runs=1)

if __name__ == "__main__":
    main()
