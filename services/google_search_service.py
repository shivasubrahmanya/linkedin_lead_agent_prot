import os
import requests
from typing import List, Dict, Any
from utils.helpers import setup_logger

logger = setup_logger("GoogleSearchService")

class GoogleSearchService:
    def __init__(self):
        self.api_key = os.getenv("SERPAPI_KEY")
        self.base_url = "https://serpapi.com/search"

    def search(self, query: str, num_results: int = 10) -> List[Dict[str, Any]]:
        """Perform a Google search using SerpAPI."""
        if not self.api_key:
            logger.warning("SERPAPI_KEY is not set. Skipping Google search.")
            return []

        params = {
            "engine": "google",
            "q": query,
            "api_key": self.api_key,
            "num": num_results
        }

        try:
            logger.info(f"Searching Google for: '{query}'")
            response = requests.get(self.base_url, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            results = data.get("organic_results", [])
            logger.info(f"Found {len(results)} results for query '{query}'")
            return results
        except requests.exceptions.RequestException as e:
            logger.error(f"Google search failed: {e}")
            return []
