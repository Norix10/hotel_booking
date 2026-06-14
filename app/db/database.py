from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

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
