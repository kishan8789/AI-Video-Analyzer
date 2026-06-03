"""Configuration management for the RAG chatbot backend."""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # OpenAI Configuration
    openai_api_key: str
    llm_model: str = "gpt-4o"
    llm_temperature: float = 0.7
    embeddings_model: str = "text-embedding-3-small"

    # YouTube Configuration (optional)
    youtube_api_key: str = ""

    # Vector DB Configuration
    vector_db_path: str = "./vector_store"

    # Backend Configuration
    backend_port: int = 8000
    backend_host: str = "0.0.0.0"
    environment: str = "development"

    # CORS
    cors_origins: list = ["http://localhost:3000", "http://localhost:3001"]

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
