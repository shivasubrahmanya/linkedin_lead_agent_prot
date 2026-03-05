import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils.helpers import setup_logger
from dotenv import load_dotenv

load_dotenv()
logger = setup_logger("EmailService")

class EmailService:
    def __init__(self):
        self.host = os.getenv("SMTP_HOST")
        self.port = int(os.getenv("SMTP_PORT", 587))
        self.user = os.getenv("SMTP_USER")
        self.password = os.getenv("SMTP_PASS")
        self.from_email = os.getenv("EMAIL_FROM")

    def send_email(self, to_email: str, subject: str, body: str) -> bool:
        """Send a plain-text email via SMTP."""
        if not all([self.host, self.user, self.password, self.from_email]):
            logger.error("SMTP configuration is incomplete. Check your .env file.")
            return False

        msg = MIMEMultipart()
        msg['From'] = self.from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP(self.host, self.port) as server:
                server.starttls()
                server.login(self.user, self.password)
                server.send_message(msg)
                logger.info(f"Email successfully sent to {to_email}")
                return True
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
            return False
