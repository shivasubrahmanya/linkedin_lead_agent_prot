from typing import Dict, Any
from utils.helpers import setup_logger

logger = setup_logger("DecisionAgent")

class DecisionAgent:
    def __init__(self):
        pass

    def determine_path(self, best_contact: Dict[str, Any]) -> str:
        """Determine outreach method."""
        
        email = best_contact.get("email")
        status = best_contact.get("status")
        score = best_contact.get("score", 0)

        # Logic: if email_valid and confidence >= 60 -> send email
        if email and status == "valid" and score >= 60:
            logger.info(f"Decision: 'email' (Score {score}, Status: {status})")
            return "email"
        else:
            logger.info(f"Decision: 'linkedin' (Score {score}, Status: {status})")
            return "linkedin"
