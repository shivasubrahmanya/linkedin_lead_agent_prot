import os
import requests
from typing import Dict, Any
from utils.helpers import setup_logger

logger = setup_logger("EmailVerifier")

class EmailVerifierService:
    def __init__(self):
        self.api_key = os.getenv("VERIFICATION_API_KEY")
        # Example using Hunter.io API. Adjust to NeverBounce or ZeroBounce as needed.
        self.endpoint = "https://api.hunter.io/v2/email-verifier"

    def verify(self, email: str) -> Dict[str, Any]:
        """Verify an email using an external API."""
        if not self.api_key:
            logger.warning("VERIFICATION_API_KEY is not set. Returning 'unverified'.")
            return {"email": email, "status": "unverified", "score": 50}

        try:
            logger.info(f"Verifying email: {email}")
            params = {
                "email": email,
                "api_key": self.api_key
            }
            response = requests.get(self.endpoint, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json().get("data", {})
                status = data.get("status", "unknown")
                score = data.get("score", 50)
                
                # Normalize status mapping (valid, invalid, accept_all/catch-all)
                if status == "valid":
                    norm_status = "valid"
                elif status == "invalid":
                    norm_status = "invalid"
                elif status == "accept_all":
                    norm_status = "catch-all"
                else:
                    norm_status = "unknown"
                    
                return {"email": email, "status": norm_status, "score": score}
            else:
                logger.warning(f"Verification API returned {response.status_code}")
                return {"email": email, "status": "unverified", "score": 50}
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to verify email {email}: {e}")
            return {"email": email, "status": "error", "score": 0}
