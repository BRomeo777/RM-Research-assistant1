from sqlalchemy import String, Text, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class Extraction(Base):
    __tablename__ = "extractions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    paper_id: Mapped[int] = mapped_column(ForeignKey("papers.id", ondelete="CASCADE"), unique=True)
    
    # Structured PICO Data
    population: Mapped[str] = mapped_column(Text, nullable=True)
    intervention: Mapped[str] = mapped_column(Text, nullable=True)
    comparator: Mapped[str] = mapped_column(Text, nullable=True)
    outcome: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Evidence Certainty & Bias
    rob_status: Mapped[str] = mapped_column(String(50), default="pending") 
    rob_details: Mapped[dict] = mapped_column(JSON, nullable=True)  # Detailed domain scores
    grade_score: Mapped[str] = mapped_column(String(50), nullable=True)
    
    # The full synthesized abstract text
    ai_summary: Mapped[str] = mapped_column(Text, nullable=True)
