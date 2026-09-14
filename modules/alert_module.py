import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import modules.logger_module as log_mod

class AlertModule:
    """Module responsible for dispatching System Alerts via Telegram or SMTP Email."""

    def __init__(self, telegram_token=None, telegram_chat_id=None, smtp_config=None):
        self.telegram_token = telegram_token
        self.telegram_chat_id = telegram_chat_id
        self.smtp_config = smtp_config or {}

        self.logger = None
        for class_name in ['SystemLogger', 'LoggerModule', 'Logger']:
            if hasattr(log_mod, class_name):
                try:
                    cls = getattr(log_mod, class_name)
                    self.logger = cls()
                    break
                except Exception:
                    pass

    def send_telegram_alert(self, message):
        """Sends a notification message to a configured Telegram chat."""
        if not self.telegram_token or not self.telegram_chat_id:
            print("[AlertModule Info] Telegram credentials missing. Skipping Telegram notification.")
            return False

        url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
        payload = {
            "chat_id": self.telegram_chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }

        try:
            response = requests.post(url, json=payload, timeout=8)
            if response.status_code == 200:
                print("[AlertModule Success] Telegram notification sent.")
                return True
            else:
                print(f"[AlertModule Error] Failed to send Telegram alert. HTTP {response.status_code}")
                return False
        except Exception as e:
            print(f"[AlertModule Error] Telegram API Exception: {str(e)}")
            return False

    def send_email_alert(self, subject, body_text):
        """Sends an email notification using SMTP configuration."""
        sender_email = self.smtp_config.get("sender_email")
        sender_password = self.smtp_config.get("sender_password")
        recipient_email = self.smtp_config.get("recipient_email")
        smtp_server = self.smtp_config.get("smtp_server", "smtp.gmail.com")
        smtp_port = self.smtp_config.get("smtp_port", 587)

        if not sender_email or not sender_password or not recipient_email:
            print("[AlertModule Info] Email credentials missing. Skipping Email notification.")
            return False

        try:
            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = recipient_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body_text, "plain"))

            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
            server.quit()

            print("[AlertModule Success] Email notification sent.")
            return True
        except Exception as e:
            print(f"[AlertModule Error] Email dispatch failed: {str(e)}")
            return False

    def notify_workflow_status(self, total_scraped, clean_records, exported_files, error_message=None):
        """Generates and dispatches a comprehensive workflow execution report."""
        if error_message:
            subject = "⚠️ Aetros Platform: Workflow Execution Error"
            msg = f"❌ *Aetros Workflow Failed*\n\n*Error Summary:* {error_message}"
        else:
            subject = "✅ Aetros Platform: Workflow Execution Success"
            msg = (
                "🚀 *Aetros Automation Workflow Completed*\n\n"
                f"• *URLs Scraped:* {total_scraped}\n"
                f"• *Clean Records Saved:* {clean_records}\n"
                f"• *Report Formats:* CSV & JSON Generated\n"
                "• *Status:* 100% Healthy"
            )

        print("\n--- Dispatching System Alerts ---")
        self.send_telegram_alert(msg)
        self.send_email_alert(subject, msg.replace("*", ""))
        print("--- Alert Dispatch Complete ---\n")
