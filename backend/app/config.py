from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://lawbridge:lawbridge@postgres:5432/lawbridge"
    REDIS_URL: str = "redis://redis:6379"
    JWT_SECRET: str = "lawbridge-v2-secret-2024"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24 * 7
    APP_NAME: str = "LawBridge AI"
    AI_PROVIDER: str = "mock"
    MOCK_AI_MODE: bool = True
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o-mini"
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-1.5-flash"
    ANTHROPIC_API_KEY: Optional[str] = None
    ANTHROPIC_MODEL: str = "claude-3-haiku-20240307"
    AI_CACHE_TTL_SECONDS: int = 86400
    AI_MAX_INPUT_CHARS: int = 15000
    AI_MAX_OUTPUT_TOKENS: int = 2000
    AI_REQUEST_TIMEOUT_SECONDS: int = 45
    MAX_UPLOAD_SIZE_MB: int = 10
    UPLOAD_DIR: str = "/app/uploads"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
