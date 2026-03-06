from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any

class ExtractionBase(BaseModel):
    population: Optional[str] = None
    intervention: Optional[str] = None
    comparator: Optional[str] = None
    outcome: Optional[str] = None
    
    rob_status: str = "pending"
    rob_details: Optional[Dict[str, Any]] = None
    grade_score: Optional[str] = None
    ai_summary: Optional[str] = None

class ExtractionCreate(ExtractionBase):
    paper_id: int

class ExtractionResponse(ExtractionBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    paper_id: int
