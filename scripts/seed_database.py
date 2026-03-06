import asyncio
import logging
import sys
import os

# Add the root directory to the Python path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import engine
from core.models.base import Base
# We must import all models here so SQLAlchemy knows they exist before creating tables
from core.models.paper import Paper
from core.models.extraction import Extraction

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("rm_research.setup")

async def init_models():
    """Creates all database tables based on our SQLAlchemy models."""
    logger.info("Initializing database schema...")
    
    async with engine.begin() as conn:
        # Warning: drop_all() wipes the database. This is fine for Phase 2 local dev.
        # Remove the drop_all line when moving to Oracle production!
        logger.info("Dropping existing tables (Dev Mode)...")
        await conn.run_sync(Base.metadata.drop_all)
        
        logger.info("Creating fresh tables...")
        await conn.run_sync(Base.metadata.create_all)
        
    logger.info("Database initialization complete! Tables created successfully.")

if __name__ == "__main__":
    # Windows/Linux compatible async loop execution
    asyncio.run(init_models())
