from typing import Dict, Any, List
from services.google_search_service import GoogleSearchService
from services.website_crawler import WebsiteCrawler
from services.email_extractor import EmailExtractor
from services.clearbit_service import ClearbitService
from services.lusha_service import LushaService
from utils.helpers import setup_logger

logger = setup_logger("DiscoveryAgent")

class DiscoveryAgent:
    def __init__(self):
        self.search_service = GoogleSearchService()
        self.crawler = WebsiteCrawler(max_pages=30, max_depth=2)
        self.extractor = EmailExtractor()
        self.clearbit_service = ClearbitService()
        self.lusha_service = LushaService()

    def discover_emails(self, profile: Dict[str, Any], domain: str) -> List[str]:
        """Find candidate emails from public sources."""
        if not profile.get("name") or not domain:
            logger.warning("Missing name or domain, skipping discovery.")
            return []

        name = profile["name"]
        company = profile["company"]
        first_name = name.split()[0] if " " in name else name

        candidate_emails = set()

        # 1. Google Search technique
        logger.info(f"Starting discovery for {name} at {domain}")
        queries = [
            f'"{name}" "@{domain}"',
            f'"{first_name}" "{company}" email',
            f'contact "team" "@{domain}"'
        ]

        # Aggregate snippets from Search
        search_text = ""
        for query in queries:
            results = self.search_service.search(query, num_results=5)
            for res in results:
                search_text += res.get("snippet", "") + " "
                
        # Extract from Google Snippets
        extracted_from_search = self.extractor.extract(search_text, filter_domain=domain)
        candidate_emails.update(extracted_from_search)

        # 2. Clearbit API Enrichment
        if not candidate_emails:
             logger.info(f"No emails from Google Search. Trying Clearbit for {name} @ {domain}...")
             clearbit_emails = self.clearbit_service.find_email(name, domain)
             candidate_emails.update(clearbit_emails)
             
        # 3. Lusha API Enrichment
        if not candidate_emails:
             logger.info(f"No emails from Clearbit. Trying Lusha for {name} @ {company}...")
             lusha_emails = self.lusha_service.find_email(name, company)
             candidate_emails.update(lusha_emails)

        # 4. Website Crawling technique (if no emails found in search snippets or APIs)
        if not candidate_emails:
            logger.info(f"No emails from APIs. Crawling domain {domain}...")
            site_text = self.crawler.crawl(f"https://{domain}")
            extracted_from_crawl = self.extractor.extract(site_text, filter_domain=domain)
            candidate_emails.update(extracted_from_crawl)

        # Optional generic templates generation as fallback
        if not candidate_emails:
            last_name = name.split()[-1] if " " in name else ""
            candidate_emails.add(f"{first_name.lower()}@{domain}")
            candidate_emails.add(f"{first_name.lower()}.{last_name.lower()}@{domain}")

        logger.info(f"Total candidate emails discovered: {list(candidate_emails)}")
        return list(candidate_emails)
