import pytest
import pytest_asyncio
from typing import Generator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.main import app
from app.core.config import settings
from app.db.database import get_db_session
from app.models.base import Base

pytest_plugins = [
    "tests.fixtures.user",
    "tests.fixtures.boking",
    "tests.fixtures.payment",
]

@pytest_asyncio.fixture(scope="function")
async def engine():
    engine = create_async_engine(settings.TEST_DB_URL, echo=settings.TEST_DB_ECHO)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def prepare_db(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def session(engine):
    async_session_maker = async_sessionmaker(engine, autoflush=False, expire_on_commit=False)
    async with async_session_maker() as session:
        yield session
        await session.flush()
        await session.rollback()


@pytest.fixture(scope="function")
def override_get_db_session(session):
    async def _override_get_db_session():
        yield session
    return _override_get_db_session


@pytest_asyncio.fixture(scope="function")
async def async_client(override_get_db_session) -> Generator:
    app.dependency_overrides[get_db_session] = override_get_db_session
    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            yield ac
    finally:
        app.dependency_overrides.clear()