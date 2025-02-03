from typing import AsyncGenerator, Generator
from unittest.mock import AsyncMock, MagicMock, Mock
from uuid import uuid4

import pytest_asyncio
from fastapi.testclient import TestClient
from main import main_app
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from api.dependencies import current_super_user, current_user
from core import db_helper
from core.base import Base
from domains.tags import Tags
from domains.users import User

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(TEST_DATABASE_URL, future=True)
session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)


@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_test_db() -> AsyncGenerator[None]:
    """Fixture to create and drop database tables for each test function.

    Creates all tables before test execution and drops them after test completion.
    Ensures clean database state for each test.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def test_session() -> AsyncGenerator[AsyncSession]:
    """Provides an async database session for test operations.

    Yields:
        AsyncSession: SQLAlchemy async session instance
    """
    async with session_factory() as session:
        yield session


@pytest_asyncio.fixture(scope="function", autouse=True)
def client(test_session: AsyncSession) -> Generator[TestClient]:
    """Test client with overridden dependencies and mock authentication.

    Features:
    - Overrides database session getter with test session
    - Provides mock regular and super user authentication
    - Automatically cleans up overrides after test execution
    """

    async def override_get_db() -> AsyncGenerator[AsyncSession]:
        """Dependency override for database session"""
        yield test_session

    def mock_current_user() -> AsyncMock:
        """Mock authentication for regular user"""
        return AsyncMock(
            return_value=User(
                id=uuid4(),
                first_name="Test",
                last_name="User",
                email="user@example.com",
            )
        )

    def mock_current_super_user() -> AsyncMock:
        """Mock authentication for superuser"""
        return AsyncMock(
            return_value=User(
                id=uuid4(),
                first_name="Admin",
                last_name="User",
                email="admin@example.com",
                is_superuser=True,
            )
        )

    # Apply dependency overrides
    main_app.dependency_overrides[db_helper.session_getter] = override_get_db
    main_app.dependency_overrides[current_user] = mock_current_user
    main_app.dependency_overrides[current_super_user] = mock_current_super_user

    # Yield test client with cleanups
    with TestClient(main_app) as client:
        yield client
    # Reset overrides after test completion
    main_app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="session")
def mock_condition_builder() -> MagicMock:
    """Mocked condition builder for query filtering tests.

    Returns:
        MagicMock: Mock object with predefined return value for create_conditions
    """
    builder = MagicMock()
    builder.create_conditions.return_value = []
    return builder


@pytest_asyncio.fixture(scope="function")
def mock_session() -> AsyncMock:
    """Mocked async database session with common method implementations.

    Includes:
    - AsyncMock for async methods (commit, execute, get)
    - Regular Mock for sync methods (add)
    """
    session = AsyncMock(spec=AsyncSession)
    session.add = Mock()
    session.commit = AsyncMock()
    session.execute = AsyncMock()
    session.get = AsyncMock()
    return session


@pytest_asyncio.fixture(scope="function")
async def test_tag(test_session: AsyncSession) -> Tags:
    """Test tag fixture providing pre-created database entries.

    Creates two sample tags:
    - Primary test tag (name="test-tag")
    - Secondary test tag (name="test-tag-2")

    Returns:
        Tags: Primary test tag object
    """
    tag = Tags(name="test-tag")
    tag2 = Tags(name="test-tag-2")
    test_session.add(tag)
    test_session.add(tag2)
    await test_session.commit()
    await test_session.refresh(tag)
    return tag
