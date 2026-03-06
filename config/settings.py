from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # App Metadata
    APP_NAME: str = "RM Research Assistant"
    DEBUG: bool = True

    # Database URLs
    DATABASE_URL: str = Field(default="sqlite+aiosqlite:///./rm_research.db")
    REDIS_URL: Optional[str] = None
    
    # API Keys 
    OPENALEX_EMAIL: str = Field(...)
    GROQ_API_KEY: Optional[str] = None
    
    # Requirement 1.1: System Performance Guardrails
    REQUEST_TIMEOUT: int = 2  # 2-second timeout per source
    MAX_CITATION_DEPTH: int = 2  # 2-generation limit
    
    # Security
    SECRET_KEY: str = "secret-key-for-dev-only"
    ALGORITHM: str = "HS256"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
