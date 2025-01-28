from unittest.mock import MagicMock

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from core.base import Base


@pytest_asyncio.fixture(scope="session")
async def test_engine():
    """Создает движок для тестов."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def test_session(test_engine: AsyncEngine):
    """Создает сессию для тестов."""
    session_factory = async_sessionmaker(bind=test_engine, expire_on_commit=False)
    async with session_factory() as session:
        yield session


@pytest_asyncio.fixture(scope="session")
def mock_condition_builder():
    """Мок ConditionBuilder."""
    builder = MagicMock()
    builder.create_conditions.return_value = []
    return builder


# @pytest.fixture
# def client(mock_service):
#     from main import main_app
#
#
#     main_app.dependency_overrides[] = override_get_db
#
#     with TestClient(main_app) as c:
#         yield c
