from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from core.config import settings


class DatabaseHelper:
    """
    A helper class for managing asynchronous database connections using SQLAlchemy.

    This class creates an async database engine and session factory, providing
    utilities for session management and connection disposal.

    Attributes:
        engine (AsyncEngine): The asynchronous SQLAlchemy engine instance.
        session_factory (async_sessionmaker[AsyncSession]):
        A factory for creating database sessions.
    """

    def __init__(
        self,
        url: str,
        echo: bool = True,
        echo_pool: bool = True,
        max_overflow: int = 10,
        pool_size: int = 10,
    ):
        """
        Initializes the database helper with configuration options.

        Args:
            url (str): The database connection URL.
            echo (bool, optional): Enable or not SQL query logging. Defaults - True.
            echo_pool (bool, optional):
            Whether to log connection pool activity. Defaults - True.
            max_overflow (int, optional): The maximum number of connections
            exceeding the pool size. Defaults - 10.
            pool_size (int, optional): The maximum number of persistent connections.
            Defaults - 10.
        """
        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )

    async def dispose(self) -> None:
        """
        Disposes of the database engine, closing all active connections.
        """
        await self.engine.dispose()

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Provides an async generator for managing the database session lifecycle.

        Yields:
            AsyncSession: A database session instance.

        Raises:
            Exception: If an error occurs during session creation.
        """
        try:
            async with self.session_factory() as session:
                yield session
        except Exception as e:
            raise e


# Initialize the database helper using settings
db_helper = DatabaseHelper(
    url=str(settings.db.url),
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
)
