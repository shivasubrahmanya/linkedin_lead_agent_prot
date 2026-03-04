from typing import List, Dict, Any
from utils.helpers import setup_logger

logger = setup_logger("ScoringAgent")

class ScoringAgent:
    def __init__(self):
        # Scoring Weights as per requirements
        self.points_official_domain = 50
        self.points_verified_api = 40
        self.points_domain_confirmed = 35
        self.points_name_match = 30
        self.points_google_indexed = 10
        self.points_penalty_catchall = -30

    def score(self, profile: Dict[str, Any], domain: str, verified_emails: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Rank reliability of discovered contacts and return the best one."""
        
        if not verified_emails:
            logger.info("No emails to score.")
            return {}

        best_email = None
        highest_score = 0
        best_status = "unknown"

        for em_dict in verified_emails:
            email = em_dict["email"]
            status = em_dict["status"]
            
            score = 0
            
            # Domain confirmation / official domain
            if email.endswith(f"@{domain}"):
                score += (self.points_official_domain + self.points_domain_confirmed)

            # API verified status
            if status == "valid":
                score += self.points_verified_api
            elif status == "catch-all":
                score += self.points_penalty_catchall

            # Name matching naive logic
            name_parts = profile.get("name", "").lower().split()
            if any(part in email for part in name_parts):
                score += self.points_name_match

            # Assume google indexed since we got them mostly from scrapes/searches
            score += self.points_google_indexed

            logger.info(f"Email {email} scored {score} with status '{status}'")

            if score > highest_score:
                highest_score = score
                best_email = email
                best_status = status

        # Final bounds check
        highest_score = max(0, min(100, highest_score))

        result = {
            "email": best_email,
            "status": best_status,
            "score": highest_score
        }
        
        logger.info(f"Best contact determined: {result}")
        return result
