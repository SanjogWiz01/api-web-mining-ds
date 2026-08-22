"""
Application configuration using pydantic-settings.
Loads values from environment variables or a .env file.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Global application settings loaded from environment."""

    APP_NAME: str = "Task Manager API"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "sqlite:///./task_manager.db"

    # JWT Authentication
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Singleton settings instance used across the application
settings = Settings()
