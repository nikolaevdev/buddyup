# buddyup/config/settings.py

import os
from pydantic import BaseModel, Field

class Settings(BaseModel):
    # Настройки PostgreSQL
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", "5432"))
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "")

    # Настройки Redis
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB: int = int(os.getenv("REDIS_DB", ""))
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "")

    # Прочие настройки
    PROJECT_NAME: str = "BuddyUp Project"
    DEBUG: bool = True

settings = Settings()
