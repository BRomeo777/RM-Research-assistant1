from pydantic import BaseModel, Field
from typing import List, Optional
from .paper import PaperResponse

class SearchQuery(BaseModel):
    q: str = Field(..., min_length=2, description="The natural language research query")
    limit: int = Field(default=20, ge=1, le=100, description="Max results to return")
    offset: int = Field(default=0, ge=0)
    year_start: Optional[int] = Field(default=None, ge=1900)
    year_end: Optional[int] = Field(default=None)

class SearchResponse(BaseModel):
    total_results: int
    took_ms: int = 0
    results: List[PaperResponse]
