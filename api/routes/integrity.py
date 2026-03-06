from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession
from api.dependencies import get_db
from api.middleware.rate_limit import limiter
from services.integrity.veritas import VeritasEngine
from fastapi import Request

router = APIRouter(tags=["Veritas Integrity (Phase 5)"])

@router.post("/verify")
@limiter.limit("2/minute") # Very heavy computation, so we limit strictly
async def check_integrity(
    request: Request,
    content: str = Body(..., embed=True),
    db: AsyncSession = Depends(get_db)
):
    """
    Scans content against the Veritas Shield to detect 
    AI-generated paraphrasing and cognitive plagiarism.
    """
    engine = VeritasEngine(db)
    report = await engine.verify_originality(content)
    return report
