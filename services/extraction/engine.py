from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.models.extraction import Extraction
from core.schemas.extraction import ExtractionResponse
from .pico import PICOExtractor
import logging

logger = logging.getLogger("rm_research.extraction.engine")

class ExtractionEngine:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.pico_extractor = PICOExtractor()

    async def process_paper(self, paper_id: int, abstract: str) -> ExtractionResponse | None:
        """Coordinates all extraction tasks for a single paper."""
        
        # 1. Check if we already extracted this paper to save API costs
        query = select(Extraction).where(Extraction.paper_id == paper_id)
        result = await self.db.execute(query)
        existing = result.scalar_one_or_none()
        
        if existing:
            logger.info(f"Extraction already exists for paper {paper_id}")
            return ExtractionResponse.model_validate(existing)

        # 2. Run the PICO Extraction
        logger.info(f"Running TrialSieve extraction for paper {paper_id}")
        pico_result = await self.pico_extractor.extract_pico(abstract)
        
        # 3. Save the new extraction to the database
        new_extraction = Extraction(
            paper_id=paper_id,
            population=pico_result.population if pico_result else None,
            intervention=pico_result.intervention if pico_result else None,
            comparator=pico_result.comparator if pico_result else None,
            outcome=pico_result.outcome if pico_result else None,
            rob_status="pending"
        )
        
        try:
            self.db.add(new_extraction)
            await self.db.commit()
            await self.db.refresh(new_extraction)
            return ExtractionResponse.model_validate(new_extraction)
        except Exception as e:
            logger.error(f"Failed to save extraction to DB: {e}")
            await self.db.rollback()
            return None
