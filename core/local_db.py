import sqlite3
import os
import datetime

class LocalDBConnector:
    """Manages local SQLite database storage for Aetros scraped data backup."""

    def __init__(self, db_path="aetros_backup.db"):
        self.db_path = db_path
        self.init_db()

    def get_connection(self):
        """Creates and returns a SQLite database connection."""
        return sqlite3.connect(self.db_path)

    def init_db(self):
        """Initializes the SQLite database table structure if it does not exist."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS scraped_backup (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT,
                        url TEXT UNIQUE,
                        title TEXT,
                        status_code INTEGER,
                        status TEXT,
                        ai_summary TEXT,
                        sentiment TEXT,
                        keywords TEXT,
                        created_at TEXT
                    )
                """)
                conn.commit()
            print(f"[LocalDB] Initialized database backup at: {self.db_path}")
        except Exception as e:
            print(f"[LocalDB Error] Initialization failed: {str(e)}")

    def save_batch_records(self, records):
        """Saves or updates scraped records into the local SQLite database in batch."""
        if not records:
            return 0

        query = """
            INSERT INTO scraped_backup (
                timestamp, url, title, status_code, status, ai_summary, sentiment, keywords, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(url) DO UPDATE SET
                timestamp=excluded.timestamp,
                title=excluded.title,
                status_code=excluded.status_code,
                status=excluded.status,
                ai_summary=excluded.ai_summary,
                sentiment=excluded.sentiment,
                keywords=excluded.keywords,
                created_at=excluded.created_at
        """

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_records = []
        for r in records:
            # Ensure proper field mapping
            if len(r) >= 8:
                formatted_records.append((r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], now))

        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.executemany(query, formatted_records)
                conn.commit()
            saved_count = len(formatted_records)
            print(f"[LocalDB Success] Backed up {saved_count} records to SQLite DB.")
            return saved_count
        except Exception as e:
            print(f"[LocalDB Error] Failed to save batch records: {str(e)}")
            return 0
