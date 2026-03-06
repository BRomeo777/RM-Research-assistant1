from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from datetime import datetime

class PaperBase(BaseModel):
    title: str = Field(..., description="The title of the academic paper")
    doi: Optional[str] = None
    authors: List[str] = Field(default_factory=list)
    journal: Optional[str] = None
    publication_date: Optional[datetime] = None
    abstract: Optional[str] = None

class PaperCreate(PaperBase):
    """Schema for inserting a new paper into the database."""
    citations_count: int = 0
    open_access_status: str = "closed"

class PaperResponse(PaperBase):
    """Schema for returning paper data to the frontend or API client."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    citations_count: int
    open_access_status: str
    created_at: datetime
