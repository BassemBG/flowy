"""Configuration module using pydantic-settings."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Hugging Face API Token
    HF_TOKEN: str = ""
    
    # ChromaDB Configuration
    CHROMA_PERSIST_DIRECTORY: str = "./chroma_data"
    CHROMA_COLLECTION: str = "glossary_terms"
    
    # Retrieval settings
    SIMILARITY_THRESHOLD: float = 0.0  # Return all results, let frontend filter
    DEFAULT_TOP_K: int = 3
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
