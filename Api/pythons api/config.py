import os


class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "Python API")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")


settings = Settings()
