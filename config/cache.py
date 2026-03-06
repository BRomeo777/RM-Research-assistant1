from typing import Any, Optional
from .logging import logger

# In-memory dictionary for Phase 1/Phase 2 fallback
_local_cache = {}

class CacheManager:
    @staticmethod
    async def get(key: str) -> Optional[Any]:
        return _local_cache.get(key)

    @staticmethod
    async def set(key: str, value: Any, ttl_seconds: int = 3600):
        _local_cache[key] = value
        logger.info(f"Cached data for key: {key}")

    @staticmethod
    async def delete(key: str):
        if key in _local_cache:
            del _local_cache[key]
