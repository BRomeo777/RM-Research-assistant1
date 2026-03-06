from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_db
from api.middleware.rate_limit import limiter
from core.schemas.search import SearchQuery, SearchResponse
from services.search.engine import SearchEngine

router = APIRouter(tags=["Discovery & Seed Intelligence"])

@router.post("/", response_model=SearchResponse)
@limiter.limit("10/minute")  # Protects your system from abuse
async def search_papers(
    request: Request,
    query: SearchQuery,
    db: AsyncSession = Depends(get_db)
):
    """
    Executes a federated search across the Open Data Core (OpenAlex).
    Checks local cache first, then falls back to external APIs.
    """
    engine = SearchEngine(db)
    results = await engine.execute_search(query)
    return results
