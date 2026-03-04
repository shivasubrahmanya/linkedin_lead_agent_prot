import os
import requests
from typing import List
from utils.helpers import setup_logger

logger = setup_logger("LushaService")

class LushaService:
    def __init__(self):
        self.api_key = os.getenv("LUSHA_API_KEY")
        self.base_url = "https://api.lusha.com/person/v2/find"

    def find_email(self, name: str, company: str) -> List[str]:
        """Attempt to find a person's email using Lusha's Person Enrichment API."""
        if not self.api_key or self.api_key == "your_lusha_api_key_here":
            logger.warning("LUSHA_API_KEY is not set or invalid. Skipping Lusha enrichment.")
            return []
            
        # Lusha often uses first and last name separately
        name_parts = name.split()
        first_name = name_parts[0] if name_parts else ""
        last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""

        payload = {
            "firstName": first_name,
            "lastName": last_name,
            "company": company
        }
        
        headers = {
            "api_key": self.api_key,
            "Content-Type": "application/json"
        }

        try:
            logger.info(f"Querying Lusha for {first_name} {last_name} at {company}...")
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                emails = []
                # Lusha typically returns a 'data' object which contains an 'emails' array
                data_obj = data.get("data", {})
                email_list = data_obj.get("emails", [])
                
                for em_obj in email_list:
                    em = em_obj.get("email")
                    if em:
                        emails.append(em)
                        
                if emails:
                    logger.info(f"Lusha found emails: {emails}")
                return emails
            elif response.status_code == 404:
                logger.debug("Lusha returned 404 Not Found.")
            else:
                 logger.warning(f"Lusha returned unexpected status: {response.status_code}")
                 
        except requests.exceptions.RequestException as e:
            logger.error(f"Lusha search failed: {e}")
            
        return []
