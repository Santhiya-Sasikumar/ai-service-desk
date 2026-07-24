import pytest
import pytest_asyncio
import httpx
from httpx import ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.pool import NullPool

from app.db.base import Base
from app.core.config import settings
from app.core.deps import get_db
from app.main import app

import sys

TEST_DATABASE_URL = settings.DATABASE_URL.replace(
    "ai_service_desk", "ai_service_desk_test"
)

# Fallback to localhost when running tests locally on Windows host
if sys.platform == "win32" and "host.docker.internal" in TEST_DATABASE_URL:
    TEST_DATABASE_URL = TEST_DATABASE_URL.replace("host.docker.internal", "localhost")

engine = create_async_engine(
    TEST_DATABASE_URL,
    poolclass=NullPool,  # fresh connection every time, no pooling conflicts
)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_test_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session():
    async with engine.connect() as conn:
        transaction = await conn.begin()
        session = AsyncSession(bind=conn, expire_on_commit=False)
        yield session
        await session.close()
        await transaction.rollback()


@pytest_asyncio.fixture
async def client(db_session):
    """
    An async HTTP client that calls the FastAPI app directly,
    on the SAME event loop as the test — no background thread involved.
    """
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac

    app.dependency_overrides.clear()