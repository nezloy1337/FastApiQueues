from datetime import datetime
from typing import AsyncGenerator, Generator
from unittest.mock import AsyncMock, MagicMock, Mock
from uuid import uuid4

import pytest_asyncio
from _pytest.monkeypatch import MonkeyPatch
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from api.dependencies import current_super_user, current_user
from core import db_helper, settings
from core.base import Base
from domains.queues import Queue, QueueEntries
from domains.users import User
from main import main_app

# Generate unique user IDs for testing
user_id = uuid4()
super_user_id = uuid4()

# Create an in-memory SQLite database for testing
TEST_DATABASE_URL = settings.test_db.url
engine = create_async_engine(TEST_DATABASE_URL, future=True)
session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)


@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_test_db() -> AsyncGenerator[None]:
    """
    Fixture to set up and tear down the test database.

    This fixture:
    - Creates all database tables before each test function.
    - Drops all database tables after each test function to ensure a clean state.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def test_session() -> AsyncGenerator[AsyncSession]:
    """
    Provides an async database session for test operations.

    Yields:
        AsyncSession: SQLAlchemy async session instance.
    """
    async with session_factory() as session:
        yield session


@pytest_asyncio.fixture(scope="function", autouse=True)
def client(
    test_session: AsyncSession, test_user: User, test_super_user: User
) -> Generator[TestClient]:
    """
    Creates a FastAPI TestClient with dependency overrides for testing.

    Features:
    - Overrides the database session dependency.
    - Provides mock authentication for regular users and superusers.
    - Cleans up overrides after each test.

    Args:
        test_session (AsyncSession): The test database session.
        test_user (User): A test regular user.
        test_super_user (User): A test superuser.

    Yields:
        TestClient: The test client instance.
    """

    async def override_get_db() -> AsyncGenerator[AsyncSession]:
        """Overrides the database session dependency."""
        yield test_session

    def mock_current_user() -> User:
        """Mocks the authentication for a regular user."""
        user = User(id=user_id, first_name="Test", last_name="super_user")
        user.id = user_id
        return user

    def mock_current_super_user() -> User:
        """Mocks the authentication for a superuser."""
        user = User(id=super_user_id, first_name="Test", last_name="super_user")
        return user

    # Apply dependency overrides
    main_app.dependency_overrides[db_helper.session_getter] = override_get_db
    main_app.dependency_overrides[current_user] = mock_current_user
    main_app.dependency_overrides[current_super_user] = mock_current_super_user

    # Yield a test client instance
    with TestClient(main_app) as client:
        yield client

    # Reset dependency overrides after the test completes
    main_app.dependency_overrides.clear()


@pytest_asyncio.fixture(autouse=True)
def patch_celery_apply_async(monkeypatch: MonkeyPatch) -> tuple[MagicMock, MagicMock]:
    # Импортируем нужные объекты
    from tasks.tasks import process_error, process_log

    # Создаём отдельные моки для каждого метода
    mock_log_apply_async = MagicMock()
    mock_error_apply_async = MagicMock()

    # Подменяем методы apply_async в Celery задачах
    monkeypatch.setattr(process_log, "apply_async", mock_log_apply_async)
    monkeypatch.setattr(process_error, "apply_async", mock_error_apply_async)

    return mock_log_apply_async, mock_error_apply_async


@pytest_asyncio.fixture(scope="function")
async def test_user(test_session: AsyncSession) -> User:
    """
    Creates a test regular user.

    Yields:
        User: A test user instance.
    """
    return User(
        id=uuid4(),
        first_name="Test",
        last_name="User",
        email="user@example.com",
    )


@pytest_asyncio.fixture(scope="function")
async def test_super_user(test_session: AsyncSession) -> User:
    """
    Creates a test superuser.

    Yields:
        User: A test superuser instance.
    """
    return User(
        id=uuid4(),
        first_name="Test",
        last_name="User",
        email="user@example.com",
    )


@pytest_asyncio.fixture(scope="function")
def mock_session() -> AsyncMock:
    """
    Mocks an async database session with standard method implementations.

    Includes:
    - AsyncMock for async methods (commit, execute, get).
    - Regular Mock for sync methods (add).

    Returns:
        AsyncMock: A mock instance of `AsyncSession`.
    """
    session = AsyncMock(spec=AsyncSession)
    session.add = Mock()
    session.commit = AsyncMock()
    session.execute = AsyncMock()
    session.get = AsyncMock()
    return session


@pytest_asyncio.fixture(scope="function")
async def test_queue(test_session: AsyncSession) -> Queue:
    """
    Creates a test queue.

    - The queue starts one year from the current date.

    Yields:
        Queue: A test queue instance.
    """
    dt = datetime.now()
    date_obj = dt.replace(year=dt.year + 1)
    queue = Queue(id=1, name="test-queue-1", start_time=date_obj, max_slots=26)
    test_session.add(queue)
    await test_session.commit()
    await test_session.refresh(queue)
    return queue


@pytest_asyncio.fixture(scope="function")
async def test_queue_entry(
    test_session: AsyncSession, test_queue: Queue
) -> QueueEntries:
    """
    Creates a test queue entry.

    Yields:
        QueueEntries: A test queue entry instance.
    """
    queue_entry = QueueEntries(position=1, queue_id=1, user_id=str(user_id))
    test_session.add(queue_entry)
    await test_session.commit()
    await test_session.refresh(queue_entry)
    return queue_entry
