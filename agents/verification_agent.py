from typing import List, Dict, Any
from services.email_verifier_service import EmailVerifierService
from utils.helpers import setup_logger

logger = setup_logger("VerificationAgent")

class VerificationAgent:
    def __init__(self):
        self.verifier = EmailVerifierService()

    def verify_emails(self, emails: List[str]) -> List[Dict[str, Any]]:
        """Verify a list of emails directly via the Verification Service."""
        results = []
        for email in emails:
            result = self.verifier.verify(email)
            results.append(result)
            
        logger.info(f"Verified {len(emails)} emails.")
        return results
