import csv
import os
import time
from services.email_service import EmailService
from storage.database import Database
from storage.csv_client import CsvClient
from utils.helpers import setup_logger
from dotenv import load_dotenv

load_dotenv()
logger = setup_logger("EmailOutreachScript")

def process_email_queue():
    db = Database()
    csv_client = CsvClient()
    email_service = EmailService()
    
    logger.info("Checking for queued emails in leads.csv...")
    
    # In a real scenario, we should fetch from DB, but the request mentioned CSV.
    # Let's read the CSV and find rows with Email Status == 'queued'
    if not os.path.exists("leads.csv"):
        logger.error("leads.csv not found.")
        return

    rows = []
    with open("leads.csv", mode='r', encoding='utf-8') as f:
        reader = list(csv.reader(f))
        if not reader:
            return
        headers = reader[0]
        rows = reader[1:]

    # Indices (based on CsvClient headers)
    # Name,Company,Role,Domain,Email,Phone,Source,Verification Status,Confidence Score,Email Status,Email Timestamp,...
    try:
        email_idx = headers.index("Email")
        status_idx = headers.index("Email Status")
        timestamp_idx = headers.index("Email Timestamp")
        name_idx = headers.index("Name")
        company_idx = headers.index("Company")
        role_idx = headers.index("Role")
    except ValueError as e:
        logger.error(f"CSV headers are missing required columns: {e}")
        return

    updated_any = False
    for i, row in enumerate(rows):
        if len(row) > status_idx and row[status_idx] == "queued" and row[email_idx]:
            to_email = row[email_idx]
            name = row[name_idx]
            company = row[company_idx]
            role = row[role_idx]
            
            logger.info(f"Processing queued email for {name} ({to_email})")
            
            # We need the subject and body. 
            # In the current main.py flow, we don't store them in the CSV yet.
            # Let's regenerate them or assume they are stored if we update main.py later.
            # For now, let's use a fallback or update the OutreachAgent/CSV to store them.
            
            from ai.message_generator import MessageGenerator
            mg = MessageGenerator()
            content = mg.create_outreach_email(name, role, company)
            
            success = email_service.send_email(to_email, content["subject"], content["body"])
            
            if success:
                row[status_idx] = "sent"
                row[timestamp_idx] = time.strftime("%Y-%m-%d %H:%M:%S")
                # Also update DB if possible (requires name/email match)
                # db.update_lead_email_status(to_email, "sent") # Assuming this exists or should be added
                updated_any = True
                logger.info(f"Marked {to_email} as sent.")
            else:
                row[status_idx] = "failed"
                updated_any = True

    if updated_any:
        with open("leads.csv", mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)
        logger.info("Updated leads.csv with email statuses.")
    else:
        logger.info("No queued emails found.")

if __name__ == "__main__":
    process_email_queue()
