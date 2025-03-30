# buddyup/models/db.py

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker
from config.settings import settings

DATABASE_URL = (
    f"postgresql+asyncpg://{settings.POSTGRES_USER}:"
    f"{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:"
    f"{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
)

engine = create_async_engine(
    DATABASE_URL,
    echo=settings.DEBUG
)

async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)

async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session
