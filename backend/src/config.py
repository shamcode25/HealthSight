from pydantic_settings import BaseSettings
from typing import ClassVar


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./healthcare.db"
    API_V1_PREFIX: str = ""
    CORS_ORIGINS: ClassVar[list[str]] = [
        "http://localhost:5173",
        "http://localhost:3000",
    ]
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"
    OPENAI_TEMPERATURE: float = 0.3

    class Config:
        env_file = ".env"


settings = Settings()
