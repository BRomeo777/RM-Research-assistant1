from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
import time
from .openalex import OpenAlexClient
from .cache_manager import SearchCacheManager
from core.schemas.search import SearchQuery, SearchResponse
from core.schemas.paper import PaperResponse
from core.enums.paper import OpenAccessStatus

class SearchEngine:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.openalex = OpenAlexClient()
        self.cache = SearchCacheManager(db)

    async def execute_search(self, query: SearchQuery) -> SearchResponse:
        """Coordinates the search across APIs and formats the response."""
        start_time = time.time()
        
        # Fetch raw data from OpenAlex
        raw_results = await self.openalex.search_works(query.q, limit=query.limit)
        
        formatted_results = []
        for i, work in enumerate(raw_results):
            # Safely extract authors
            authors = [
                authorship.get("author", {}).get("display_name", "Unknown")
                for authorship in work.get("authorships", [])
            ]
            
            # Format publication date
            pub_date_str = work.get("publication_date")
            pub_date = datetime.strptime(pub_date_str, "%Y-%m-%d") if pub_date_str else None

            # Determine Open Access status
            oa_data = work.get("open_access", {})
            oa_status = oa_data.get("oa_status", "closed")
            # Map OpenAlex status to our Enum safely
            try:
                mapped_oa_status = OpenAccessStatus(oa_status)
            except ValueError:
                mapped_oa_status = OpenAccessStatus.CLOSED

            # Format into our internal Pydantic Schema
            paper = PaperResponse(
                id=i + 1,  # Temporary ID since we aren't saving to DB just yet
                title=work.get("title", "Untitled Work"),
                doi=work.get("doi"),
                authors=authors,
                journal=work.get("primary_location", {}).get("source", {}).get("display_name"),
                publication_date=pub_date,
                citations_count=work.get("cited_by_count", 0),
                open_access_status=mapped_oa_status,
                created_at=datetime.now(timezone.utc)
            )
            formatted_results.append(paper)

        took_ms = int((time.time() - start_time) * 1000)

        return SearchResponse(
            total_results=len(formatted_results),
            took_ms=took_ms,
            results=formatted_results
        )
