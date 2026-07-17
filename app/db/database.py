from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_async_engine(
    settings.DB_URL,
    future=True,
    echo=settings.ECHO,
    connect_args={
        "statement_cache_size": 0,
    },
)

AsyncSession = async_sessionmaker(engine, autoflush=False, expire_on_commit=False)


async def get_db_session() -> AsyncGenerator:
    async with AsyncSession() as session:
        yield session


SYNC_DB_URL = settings.DB_URL.replace("postgresql+asyncpg://", "postgresql+psycopg://")

sync_engine = create_engine(
    SYNC_DB_URL,
    future=True,
    echo=settings.ECHO,
    pool_pre_ping=True,
)

SyncSessionLocal = sessionmaker(
    bind=sync_engine, autoflush=False, expire_on_commit=False
)
