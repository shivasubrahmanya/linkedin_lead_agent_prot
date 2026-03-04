import re
from typing import List, Set
from utils.regex_patterns import EMAIL_PATTERN
from utils.helpers import setup_logger, clean_text

logger = setup_logger("EmailExtractor")

class EmailExtractor:
    def __init__(self):
        pass

    def extract(self, text: str, filter_domain: str = None) -> List[str]:
        """Extract unique emails from text."""
        cleaned = clean_text(text)
        emails = EMAIL_PATTERN.findall(cleaned)
        
        unique_emails = {email.lower() for email in emails}
        
        if filter_domain:
            filter_domain = filter_domain.lower()
            # Only keep emails that match the company domain
            filtered = {email for email in unique_emails if email.endswith(f"@{filter_domain}")}
            logger.info(f"Extracted {len(filtered)} emails matching domain {filter_domain}")
            return list(filtered)
            
        logger.info(f"Extracted {len(unique_emails)} total emails")
        return list(unique_emails)

    def extract_from_html(self, html_content: str, filter_domain: str = None) -> List[str]:
        """Convenience method to extract directly from HTML."""
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")
        text = soup.get_text(separator=" ")
        return self.extract(text, filter_domain)
