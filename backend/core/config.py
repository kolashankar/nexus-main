from pydantic_settings import BaseSettings
from typing import List, Union
from pydantic import field_validator
import os

class Settings(BaseSettings):
    # App
    APP_NAME: str = "Karma Nexus 2.0"
    DEBUG: bool = True
    VERSION: str = "1.0.0"

    # Database
    MONGO_URL: str = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    DB_NAME: str = os.environ.get('DB_NAME', 'karma_nexus')

    # Security
    SECRET_KEY: str = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    CORS_ORIGINS: str = "*"
    ALLOWED_ORIGINS: Union[List[str], str] = ["http://localhost:3000", "http://localhost:8001", "https://adventure-rewards-1.preview.emergentagent.com"]
    
    @field_validator('ALLOWED_ORIGINS', mode='before')
    @classmethod
    def parse_allowed_origins(cls, v):
        """Parse ALLOWED_ORIGINS from comma-separated string or list."""
        if isinstance(v, str):
            # Split by comma and strip whitespace
            return [origin.strip() for origin in v.split(',') if origin.strip()]
        return v

    # AI
    GEMINI_API_KEY: str = ""

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # WebSocket
    WS_MAX_CONNECTIONS: int = 100

    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    # Logging
    LOG_LEVEL: str = "INFO"

    # Game Constants
    MAX_TRAITS: int = 80
    MAX_SUPERPOWERS: int = 25
    STARTING_CREDITS: int = 1000
    STARTING_KARMA: int = 0

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"

settings = Settings()

def get_settings() -> Settings:
    """Get application settings instance."""
    return settings
