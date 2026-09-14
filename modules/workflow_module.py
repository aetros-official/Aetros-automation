import sys
import os
from datetime import datetime

# Ensure core module is accessible
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.db_connector import AetrosDB

class WorkflowManager:
    def __init__(self):
        self.db = AetrosDB()

    def add_task(self, task_id, task_name, status="Pending"):
        """Add a new task to the Workflows sheet"""
        last_run = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row_data = [task_id, task_name, status, last_run]
        self.db.append_row("Workflows", row_data)
        print(f"[WORKFLOW] Task Added: {task_id} - {task_name} ({status})")

    def get_all_tasks(self):
        """Fetch all tasks from the Workflows sheet"""
        sheet = self.db.get_worksheet("Workflows")
        return sheet.get_all_records()

if __name__ == "__main__":
    wf = WorkflowManager()
    wf.add_task("TASK-001", "Initial System Verification", "Completed")
