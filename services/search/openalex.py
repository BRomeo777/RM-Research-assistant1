import httpx
from typing import List, Dict, Any
import logging
from config.settings import settings

logger = logging.getLogger("rm_research.search.openalex")

class OpenAlexClient:
    def __init__(self):
        self.base_url = "https://api.openalex.org/works"
        self.headers = {"User-Agent": f"mailto:{settings.OPENALEX_EMAIL}"}
        # Enforcing the 2-second timeout from Requirement 1.1
        self.timeout = httpx.Timeout(settings.REQUEST_TIMEOUT)

    async def search_works(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Fetches papers from OpenAlex based on a natural language query."""
        params = {
            "search": query,
            "per-page": limit,
            "mailto": settings.OPENALEX_EMAIL,
            "sort": "cited_by_count:desc" # Defaulting to high-impact papers
        }
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(
                    self.base_url, 
                    params=params, 
                    headers=self.headers
                )
                response.raise_for_status()
                data = response.json()
                return data.get("results", [])
            except httpx.TimeoutException:
                logger.error(f"OpenAlex timeout after {settings.REQUEST_TIMEOUT}s for query: {query}")
                return []
            except httpx.HTTPError as e:
                logger.error(f"OpenAlex API error: {e}")
                return []
