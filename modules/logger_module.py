import sys
import os
from datetime import datetime

# Parent directory ko Python path men add krna
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.db_connector import AetrosDB

class AetrosLogger:
    def __init__(self):
        self.db = AetrosDB()

    def log_event(self, level, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row_data = [timestamp, level.upper(), message]
       
        # Google Sheets ke Logs tab men entry add krna
        self.db.append_row("Logs", row_data)
        print(f"[{timestamp}] [{level.upper()}] {message}")

if __name__ == "__main__":
    logger = AetrosLogger()
    logger.log_event("INFO", "Logger Module standalone execution test.")