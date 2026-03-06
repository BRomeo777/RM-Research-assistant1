from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from api.dependencies import get_db

router = APIRouter(tags=["System Diagnostics"])

@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    """Deep health check verifying API and Database status."""
    db_status = "offline"
    try:
        await db.execute(text("SELECT 1"))
        db_status = "online"
    except Exception as e:
        db_status = f"error: {str(e)}"

    return {
        "status": "healthy",
        "database": db_status,
        "version": "1.0.0",
        "service": "RM Research Assistant Core"
    }
