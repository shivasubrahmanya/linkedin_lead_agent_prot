import os
import requests
from typing import Optional, List
from utils.helpers import setup_logger

logger = setup_logger("ClearbitService")

class ClearbitService:
    def __init__(self):
        self.api_key = os.getenv("CLEARBIT_API_KEY")
        self.base_url = "https://person.clearbit.com/v2/people/find"

    def find_email(self, name: str, domain: str) -> List[str]:
        """Attempt to find a person's email using Clearbit Discovery."""
        if not self.api_key or self.api_key == "your_clearbit_api_key_here":
            logger.warning("CLEARBIT_API_KEY is not set or invalid. Skipping Clearbit enrichment.")
            return []

        # Clearbit expects full name and company domain
        params = {
            "name": name,
            "company": domain
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        try:
            logger.info(f"Querying Clearbit for {name} @ {domain}...")
            # Note: Clearbit's person/find endpoint can sometimes take time or return 202 (queued).
            response = requests.get(self.base_url, headers=headers, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                email = data.get("email")
                if email:
                    logger.info(f"Clearbit found email: {email}")
                    return [email]
            elif response.status_code == 202:
                 logger.info("Clearbit returned 202 Queued. Data not immediately available.")
            elif response.status_code == 404:
                logger.debug("Clearbit returned 404 Not Found.")
            else:
                 logger.warning(f"Clearbit returned unexpected status: {response.status_code}")
                 
        except requests.exceptions.RequestException as e:
            logger.error(f"Clearbit search failed: {e}")
            
        return []
