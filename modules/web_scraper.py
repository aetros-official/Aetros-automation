import datetime
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from playwright.sync_api import sync_playwright
import core.db_connector as db_conn
from core.local_db import LocalDBConnector
import modules.logger_module as log_mod
from modules.ai_processor import AIProcessorModule

class WebScraperModule:
    """High-performance batch web scraper supporting Static HTML & Dynamic JS Rendering via Playwright."""
   
    def __init__(self, max_workers=5):
        self.max_workers = max_workers
        self.ai_engine = AIProcessorModule()
        self.local_db = LocalDBConnector()
        self.db = None
       
        for class_name in ['AetrosDB', 'SheetConnector', 'GoogleSheetConnector', 'DBConnector']:
            if hasattr(db_conn, class_name):
                try:
                    cls = getattr(db_conn, class_name)
                    self.db = cls()
                    print(f"[DB Connected] Connected via class: {class_name}")
                    break
                except Exception as e:
                    print(f"[DB Connection Error]: {str(e)}")

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        }

    def fetch_dynamic_page(self, url):
        """Scrapes dynamic JavaScript heavy websites using Playwright Headless Browser."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url, timeout=15000, wait_until="domcontentloaded")
                title = page.title().strip() if page.title() else "No Title Found"
                browser.close()

            ai_res = self.ai_engine.process_scraped_record(title, url)
            print(f"[Playwright JS Scraped] {url}")
            return [
                timestamp, url, title, 200, "Success (Dynamic JS)",
                ai_res["Summary"], ai_res["Sentiment"], ai_res["Keywords"]
            ]
        except Exception as e:
            ai_res = self.ai_engine.process_scraped_record("Error", url)
            return [
                timestamp, url, "Error", 500, f"JS Render Error: {str(e)}",
                ai_res["Summary"], ai_res["Sentiment"], ai_res["Keywords"]
            ]

    def fetch_page_details(self, url):
        """Attempts static HTTP fetch first, falls back to Playwright JS rendering if needed."""
        for attempt in range(1, 3):
            try:
                response = requests.get(url, headers=self.headers, timeout=8)
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
               
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    title = soup.title.string.strip() if soup.title else "No Title Found"
                   
                    # Fallback to Playwright if static HTML response lacks proper rendered title/content
                    if title in ["No Title Found", "", "N/A"]:
                        return self.fetch_dynamic_page(url)

                    status = "Success"
                    ai_res = self.ai_engine.process_scraped_record(title, url)
                    return [
                        timestamp, url, title, response.status_code, status,
                        ai_res["Summary"], ai_res["Sentiment"], ai_res["Keywords"]
                    ]
                else:
                    return self.fetch_dynamic_page(url)

            except Exception:
                if attempt == 2:
                    # Fallback to Playwright Headless Browser on HTTP failure/timeout
                    return self.fetch_dynamic_page(url)

    def save_batch_to_sheet(self, rows_data):
        """Appends all scraped rows with AI metadata to Google Sheets and SQLite DB."""
        if not rows_data:
            return

        self.local_db.save_batch_records(rows_data)

        if self.db:
            try:
                sheet_obj = getattr(self.db, 'sheet', None) or getattr(self.db, 'spreadsheet', None)
                if sheet_obj:
                    try:
                        worksheet = sheet_obj.worksheet("Scraped_Data")
                    except Exception:
                        worksheet = sheet_obj.get_worksheet(0)

                    headers = ["Timestamp", "URL", "Title", "Status Code", "Status", "AI Summary", "Sentiment", "Keywords"]
                    existing_headers = worksheet.row_values(1)
                    if not existing_headers:
                        worksheet.append_row(headers)

                    worksheet.append_rows(rows_data)
                    print(f"[Success] Saved batch of {len(rows_data)} AI-enriched records to sheet.")
                else:
                    print("[DB Error] Could not access sheet object.")
            except Exception as e:
                print(f"[Save Error] Failed batch save to sheet: {str(e)}")

    def scrape_multiple_urls(self, url_list):
        """Executes multi-threaded URL scraping with JS rendering fallback."""
        print(f"\n--- Scraping {len(url_list)} URLs with JS Rendering Engine ---")
        results = []
       
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_url = {executor.submit(self.fetch_page_details, url): url for url in url_list}
            for future in as_completed(future_to_url):
                res = future.result()
                if res:
                    results.append(res)
                    print(f"[Scraped & Processed] {res[1]} -> Sentiment: {res[6]}")

        self.save_batch_to_sheet(results)
        print("--- Batch Scraping Complete ---\n")
        return results
