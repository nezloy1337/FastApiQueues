import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from core import settings
from core.base import Base


@pytest.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(settings.TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture
async def db_session(test_engine):
    async with AsyncSession(test_engine) as session:
        transaction = await session.begin()
        yield session
        await transaction.rollback()


@pytest.fixture
def test_client(db_session):
    from app.core.database import get_db
    from app.main import app

    app.dependency_overrides[get_db] = lambda: db_session
    from fastapi.testclient import TestClient

    return TestClient(app)
