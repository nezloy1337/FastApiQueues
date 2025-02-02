from unittest.mock import AsyncMock, MagicMock, Mock
from uuid import uuid4

import pytest_asyncio
from fastapi.testclient import TestClient
from main import main_app
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from api.dependencies import current_super_user, current_user
from core import db_helper
from core.base import Base
from domains.users import User

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(TEST_DATABASE_URL, future=True)
session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_test_db():
    """Создаёт таблицы перед всеми тестами и удаляет после."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def test_session():
    """Асинхронная сессия для тестов."""
    async with session_factory() as session:
        yield session


@pytest_asyncio.fixture(scope="function", autouse=True)
def client(test_session):
    """Переопределяем db_helper.session_getter,"""

    async def override_get_db():
        yield test_session

    def mock_current_user():
        """Фейковый пользователь для тестов."""
        return AsyncMock(
            return_value=User(
                id=uuid4(),
                first_name="first_name",
                last_name="last_name",
                email="test@example.com",
            )
        )

    def mock_current_super_user():
        """Фейковый пользователь для тестов."""
        return AsyncMock(
            return_value=User(
                id=uuid4(),
                first_name="first_name",
                last_name="last_name",
                email="test@example.com",
                is_superuser=True,
            )
        )

    main_app.dependency_overrides[db_helper.session_getter] = override_get_db
    main_app.dependency_overrides[current_user] = mock_current_user
    main_app.dependency_overrides[current_super_user] = mock_current_super_user
    with TestClient(main_app) as client:
        yield client
    main_app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="session")
def mock_condition_builder():
    """Мок ConditionBuilder."""
    builder = MagicMock()
    builder.create_conditions.return_value = []
    return builder


@pytest_asyncio.fixture(scope="function")
def mock_session():
    """Мокнутый AsyncSession с правильными методами."""
    session = AsyncMock(spec=AsyncSession)
    session.add = Mock()
    session.commit = AsyncMock()
    session.execute = AsyncMock()
    session.get = AsyncMock()
    return session
