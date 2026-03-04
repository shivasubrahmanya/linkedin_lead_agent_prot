import tldextract
from typing import Optional
from services.google_search_service import GoogleSearchService
from utils.helpers import setup_logger

logger = setup_logger("CompanyAgent")

class CompanyAgent:
    def __init__(self):
        self.search_service = GoogleSearchService()

    def resolve_domain(self, company_name: str) -> Optional[str]:
        """Resolve a company name to its primary domain using Google Search."""
        if not company_name or company_name.lower() == "unknown":
            return None
            
        logger.info(f"Resolving domain for company: {company_name}")
        query = f"{company_name} official website"
        results = self.search_service.search(query, num_results=3)

        for result in results:
            url = result.get("link", "")
            if url and "linkedin.com" not in url and "wikipedia.org" not in url:
                extracted = tldextract.extract(url)
                if extracted.domain and extracted.suffix:
                    domain = f"{extracted.domain}.{extracted.suffix}"
                    logger.info(f"Resolved {company_name} to domain {domain}")
                    return domain
                    
        logger.warning(f"Could not resolve domain for {company_name}")
        return None
