from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field

from api.dependencies import get_db
from api.middleware.rate_limit import limiter
from core.schemas.extraction import ExtractionResponse
from services.extraction.engine import ExtractionEngine
from fastapi import Request

router = APIRouter(tags=["TrialSieve Extraction"])

# A simple request schema for testing
class ExtractionRequest(BaseModel):
    paper_id: int = Field(..., description="The ID of the paper in your database")
    abstract: str = Field(..., min_length=50, description="The full text abstract to analyze")

@router.post("/", response_model=ExtractionResponse)
@limiter.limit("5/minute")  # Stricter limit since LLM calls cost money/compute
async def extract_paper_data(
    request: Request,
    payload: ExtractionRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Analyzes an abstract using TrialSieve (Llama3) to extract PICO elements.
    Results are automatically saved to the database to prevent duplicate processing.
    """
    engine = ExtractionEngine(db)
    result = await engine.process_paper(payload.paper_id, payload.abstract)
    
    if not result:
        raise HTTPException(status_code=500, detail="Extraction failed. Check API keys and logs.")
        
    return result
