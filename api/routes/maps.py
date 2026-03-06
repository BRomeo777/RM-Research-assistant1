from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request

from api.dependencies import get_db
from api.middleware.rate_limit import limiter
from services.maps.engine import MapEngine

router = APIRouter(tags=["Citation Maps (Phase 4)"])

@router.get("/")
@limiter.limit("5/minute") # Strict limit because snowballing makes multiple API calls
async def get_citation_map(
    request: Request,
    seed_doi: str = Query(..., description="The exact DOI of the seed paper to map"),
    db: AsyncSession = Depends(get_db)
):
    """
    Generates a 2-generation forward and backward citation map 
    formatted for frontend network visualization (D3.js / Sigma.js).
    """
    try:
        engine = MapEngine(db)
        graph_data = await engine.generate_citation_map(seed_doi)
        
        if not graph_data.get("nodes"):
            raise HTTPException(status_code=404, detail="No citation data found for this DOI.")
            
        return graph_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Map generation failed: {str(e)}")
