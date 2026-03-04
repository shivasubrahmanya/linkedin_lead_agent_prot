import requests
from bs4 import BeautifulSoup
from typing import List, Set
from urllib.parse import urljoin, urlparse
from utils.helpers import setup_logger

logger = setup_logger("WebsiteCrawler")

class WebsiteCrawler:
    def __init__(self, max_pages: int = 20, max_depth: int = 2):
        self.max_pages = max_pages
        self.max_depth = max_depth
        
        # High-value paths to prioritize checking
        self.priority_paths = [
            "/team", "/about", "/about-us", "/contact", "/contact-us", 
            "/leadership", "/blog"
        ]

    def crawl(self, start_url: str) -> str:
        """Crawl a website and extract text from high-priority pages."""
        if not start_url.startswith("http"):
            start_url = f"https://{start_url}"

        domain = urlparse(start_url).netloc
        visited_urls = set()
        urls_to_visit = [(start_url, 0)]
        
        # Pre-seed priority URLs
        for path in self.priority_paths:
            urls_to_visit.append((urljoin(start_url, path), 1))

        all_text = []
        pages_crawled = 0

        logger.info(f"Starting crawl for {start_url}")

        while urls_to_visit and pages_crawled < self.max_pages:
            current_url, depth = urls_to_visit.pop(0)

            if current_url in visited_urls or depth > self.max_depth:
                continue

            # Ensure we stay on the same domain
            if urlparse(current_url).netloc != domain:
                continue

            try:
                response = requests.get(current_url, timeout=10)
                visited_urls.add(current_url)
                
                if response.status_code != 200:
                    continue

                pages_crawled += 1
                soup = BeautifulSoup(response.text, "html.parser")
                
                # Remove script, style, header, footer, etc.
                for script in soup(["script", "style", "header", "footer", "nav"]):
                    script.extract()
                    
                text = soup.get_text(separator=" ")
                all_text.append(text)

                # Extract more links if under depth limit
                if depth < self.max_depth:
                    for link in soup.find_all("a", href=True):
                        full_url = urljoin(current_url, link["href"])
                        if full_url not in visited_urls:
                            urls_to_visit.append((full_url, depth + 1))

            except requests.exceptions.RequestException as e:
                logger.debug(f"Failed to crawl {current_url}: {e}")
                visited_urls.add(current_url) # Mark failed as visited
                
        logger.info(f"Crawled {pages_crawled} pages for {domain}")
        return " ".join(all_text)
