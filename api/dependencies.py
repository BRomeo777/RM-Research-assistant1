from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from api.middleware.rate_limit import limiter
from config.database import SessionLocal

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Provides a fresh, async database session for each request."""
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
