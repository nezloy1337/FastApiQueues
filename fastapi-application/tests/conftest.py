from datetime import datetime
from typing import AsyncGenerator, Generator
from unittest.mock import AsyncMock, MagicMock, Mock
from uuid import uuid4

import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from api.dependencies import current_super_user, current_user
from core import db_helper
from core.base import Base
from domains.queues import Queue, QueueEntries
from domains.tags import Tags
from domains.users import User
from main import main_app

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(TEST_DATABASE_URL, future=True)
session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)

user_id = uuid4()
super_user_id = uuid4()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_test_db() -> AsyncGenerator[None]:
    """
    Fixture to create and drop database tables for each test function.
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
def client(
    test_session: AsyncSession, test_user: User, test_super_user: User
) -> Generator[TestClient]:
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
        user = MagicMock(return_value=test_user)
        user.id = user_id
        return user

    def mock_current_super_user() -> AsyncMock:
        """Mock authentication for superuser"""
        user = MagicMock(return_value=test_user)
        user.id = super_user_id
        return user

    # Apply dependency overrides
    main_app.dependency_overrides[db_helper.session_getter] = override_get_db
    main_app.dependency_overrides[current_user] = mock_current_user
    main_app.dependency_overrides[current_super_user] = mock_current_super_user

    # Yield test client with cleanups
    with TestClient(main_app) as client:
        yield client
    # Reset overrides after test completion
    main_app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="function")
async def test_user(test_session: AsyncSession) -> User:
    return User(
        id=uuid4(),
        first_name="Test",
        last_name="User",
        email="user@example.com",
    )


@pytest_asyncio.fixture(scope="function")
async def test_super_user(test_session: AsyncSession) -> User:
    return User(
        id=uuid4(),
        first_name="Test",
        last_name="User",
        email="user@example.com",
    )


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


@pytest_asyncio.fixture(scope="function")
async def test_queue(test_session: AsyncSession):
    dt = datetime.now()
    date_obj = dt.replace(year=dt.year + 1)
    queue = Queue(id=1, name="test-queue-1", start_time=date_obj, max_slots=26)
    test_session.add(queue)

    await test_session.commit()
    await test_session.refresh(queue)

    return queue


@pytest_asyncio.fixture(scope="function")
async def test_queue_entry(test_session: AsyncSession, test_queue: Queue):

    queue_entry = QueueEntries(position=1, queue_id=1, user_id=str(user_id))
    test_session.add(queue_entry)

    await test_session.commit()
    await test_session.refresh(queue_entry)

    return queue_entry
