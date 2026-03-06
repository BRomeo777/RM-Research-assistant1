from sqlalchemy import String, Text, DateTime, JSON, Index
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime
from .base import Base

class Paper(Base):
    __tablename__ = "papers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    doi: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    authors: Mapped[list] = mapped_column(JSON, nullable=False)  # Stored as a JSON array
    journal: Mapped[str] = mapped_column(String(500), nullable=True)
    publication_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    abstract: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Discovery & Propagation Tracking
    citations_count: Mapped[int] = mapped_column(default=0)
    open_access_status: Mapped[str] = mapped_column(String(50), default="closed")
    
    # Phase 5: Veritas Fingerprint (Stored securely in the DB)
    semantic_fingerprint: Mapped[list] = mapped_column(JSON, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Indexes to ensure sub-100ms query responses
    __table_args__ = (
        Index("ix_paper_title_date", "title", "publication_date"),
    )
