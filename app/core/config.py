from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENV: str = "dev"
    DATABASE_URL: str = "sqlite:///./news.db"  # swap with Postgres in prod
    # e.g. "postgresql+psycopg://user:pass@localhost:5432/news"
    ALLOW_ORIGINS: list[str] = ["*"]
    USE_CELERY: bool = False  # flip to True when Celery running

    class Config:
        env_file = ".env"

settings = Settings()