from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.models.paper import Paper
import logging

logger = logging.getLogger("rm_research.search.cache")

class SearchCacheManager:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def check_local_cache(self, doi: str) -> Paper | None:
        """Checks if a paper already exists in our local database."""
        if not doi:
            return None
            
        try:
            query = select(Paper).where(Paper.doi == doi)
            result = await self.db.execute(query)
            paper = result.scalar_one_or_none()
            
            if paper:
                logger.info(f"Cache hit for DOI: {doi}")
            return paper
        except Exception as e:
            logger.error(f"Database cache error: {e}")
            return None
