import os
import time
import schedule
from dotenv import load_dotenv

# Load Env Vars
load_dotenv()

from agents.ingestion_agent import IngestionAgent
from agents.profile_agent import ProfileAgent
from agents.company_agent import CompanyAgent
from agents.discovery_agent import DiscoveryAgent
from agents.verification_agent import VerificationAgent
from agents.scoring_agent import ScoringAgent
from agents.decision_agent import DecisionAgent
from agents.outreach_agent import OutreachAgent
from storage.database import Database
from storage.csv_client import CsvClient
from utils.helpers import setup_logger

logger = setup_logger("MainPipeline")

class LinkedInOutreachSystem:
    def __init__(self):
        logger.info("Initializing LinkedIn Outreach System components...")
        self.ingestion = IngestionAgent()
        self.profile = ProfileAgent()
        self.company = CompanyAgent()
        self.discovery = DiscoveryAgent()
        self.verification = VerificationAgent()
        self.scoring = ScoringAgent()
        self.decision = DecisionAgent()
        self.outreach = OutreachAgent()
        
        self.db = Database()
        self.csv = CsvClient()

    def process_pdf(self, pdf_path: str):
        """Run the end-to-end pipeline for a single PDF."""
        logger.info("="*50)
        logger.info(f"STARTING PIPELINE FOR: {pdf_path}")
        
        # 1. Parse Profile
        parsed_data = self.profile.parse(pdf_path)
        name = parsed_data.get("name")
        company_name = parsed_data.get("company")
        
        if not name or name == "Unknown" or not company_name or company_name == "Unknown":
            logger.warning(f"Could not extract sufficient structured data from {pdf_path}. Skipping.")
            self.ingestion.mark_processed(pdf_path)
            return

        # 2. Resolve Domain
        domain = self.company.resolve_domain(company_name)
        if not domain:
            logger.warning(f"Could not resolve domain for {company_name}. Outputting fallback data.")
            domain = ""

        # 3. Discover Emails
        candidate_emails = self.discovery.discover_emails(parsed_data, domain) if domain else []

        # 4. Verify Emails
        verified_emails = self.verification.verify_emails(candidate_emails)

        # 5. Score Confidence
        best_contact = self.scoring.score(parsed_data, domain, verified_emails)
        if not best_contact:
            best_contact = {"email": "", "status": "unknown", "score": 0}

        # 6. Decide Outreach Method
        action = self.decision.determine_path(best_contact)

        # 7. Execute Outreach (Draft)
        outreach_result = self.outreach.handle_outreach(action, parsed_data, best_contact)

        # 8. Build Final Row for Storage
        lead_row = {
            "name": name,
            "company": company_name,
            "role": parsed_data.get("role", ""),
            "domain": domain,
            "email": best_contact.get("email", ""),
            "phone": "", # Can add phone discovery logic later
            "source": "PDF Processing",
            "verification_status": best_contact.get("status", ""),
            "confidence_score": best_contact.get("score", 0),
            "email_status": "queued" if outreach_result.get("email_queued") else "",
            "linkedin_url": parsed_data.get("linkedin", ""),
            "linkedin_message": outreach_result.get("linkedin_message", ""),
            "linkedin_status": "ready" if action == "linkedin" else ""
        }

        # 9. Store in SQLite Database
        db_id = self.db.add_lead(lead_row)
        logger.info(f"Saved lead to local DB with ID: {db_id}")

        # 10. Store in local CSV
        csv_row = [
            lead_row["name"],
            lead_row["company"],
            lead_row["role"],
            lead_row["domain"],
            lead_row["email"],
            lead_row["phone"],
            lead_row["source"],
            lead_row["verification_status"],
            lead_row["confidence_score"],
            lead_row["email_status"],
            "", # Email Timestamp
            lead_row["linkedin_url"],
            lead_row["linkedin_message"],
            lead_row["linkedin_status"],
            "", # LinkedIn Timestamp
            ""  # Reply Status
        ]
        self.csv.append_row(csv_row)

        # 11. Move to Processed
        self.ingestion.mark_processed(pdf_path)
        logger.info(f"FINISHED PIPELINE FOR: {pdf_path}")
        logger.info("="*50)

    def scan_and_run(self):
        """Scan input folder and process all pending PDFs."""
        logger.info("Scanning for new PDFs...")
        pending_pdfs = self.ingestion.scan_folder()
        for pdf in pending_pdfs:
            self.process_pdf(pdf)

def start_scheduler():
    logger.info("Starting scheduler...")
    system = LinkedInOutreachSystem()
    
    # Run once immediately
    system.scan_and_run()
    
    # Schedule repeating interval
    schedule.every(10).minutes.do(system.scan_and_run)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="LinkedIn Outreach Agent")
    parser.add_argument('--run-once', action='store_true', help='Run the pipeline once and exit.')
    
    args = parser.parse_args()
    
    if args.run_once:
        system = LinkedInOutreachSystem()
        system.scan_and_run()
    else:
        start_scheduler()
