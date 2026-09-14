import time
import datetime
import core.db_connector as db_conn
import modules.logger_module as log_mod

class SchedulerModule:
    """Module responsible for running automated workflows on fixed intervals or specific schedules."""
   
    def __init__(self):
        self.db = None
        for class_name in ['AetrosDB', 'SheetConnector', 'GoogleSheetConnector', 'DBConnector']:
            if hasattr(db_conn, class_name):
                try:
                    cls = getattr(db_conn, class_name)
                    self.db = cls()
                    print(f"[Scheduler] Connected to DB via: {class_name}")
                    break
                except Exception as e:
                    print(f"[Scheduler DB Error]: {str(e)}")

        self.logger = None
        for class_name in ['SystemLogger', 'LoggerModule', 'Logger']:
            if hasattr(log_mod, class_name):
                try:
                    cls = getattr(log_mod, class_name)
                    self.logger = cls()
                    break
                except Exception:
                    pass

    def run_interval_job(self, task_function, interval_seconds=10, max_runs=3):
        """Runs a passed function repeatedly after a specified interval in seconds."""
        print(f"\n=== Starting Scheduler Job (Interval: {interval_seconds}s | Max Runs: {max_runs}) ===")
       
        run_count = 0
        while run_count < max_runs:
            run_count += 1
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n[Scheduler] Executing Run #{run_count} of {max_runs} at {timestamp}")
           
            try:
                task_function()
                print(f"[Scheduler Success] Run #{run_count} completed.")
            except Exception as e:
                print(f"[Scheduler Error] Task failed during run #{run_count}: {str(e)}")

            if run_count < max_runs:
                print(f"[Scheduler] Waiting {interval_seconds} seconds until next run...")
                time.sleep(interval_seconds)

        print("\n=== Scheduler Job Finished All Executions ===")
