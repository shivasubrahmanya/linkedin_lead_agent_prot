from ai.message_generator import MessageGenerator
from typing import Dict, Any
from utils.helpers import setup_logger

logger = setup_logger("OutreachAgent")

class OutreachAgent:
    def __init__(self):
        self.message_gen = MessageGenerator()

    def handle_outreach(self, path: str, profile: Dict[str, Any], best_contact: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the determined outreach strategy."""
        result = {
            "outreach_type": path,
            "linkedin_message": "",
            "email_queued": False
        }

        if path == "email":
            logger.info(f"Generating email for {best_contact.get('email')}")
            name = profile.get("name", "there")
            role = profile.get("role", "Professional")
            company = profile.get("company", "your company")
            
            email_content = self.message_gen.create_outreach_email(name, role, company)
            result["email_queued"] = True
            result["email_subject"] = email_content["subject"]
            result["email_body"] = email_content["body"]
            
        elif path == "linkedin":
            name = profile.get("name", "there")
            role = profile.get("role", "Professional")
            company = profile.get("company", "your company")
            
            logger.info("Generating LinkedIn Message via Ollama...")
            draft = self.message_gen.create_linkedin_dm(name, role, company)
            result["linkedin_message"] = draft
            
        return result
