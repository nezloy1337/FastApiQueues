from typing import TYPE_CHECKING, Annotated, AsyncGenerator

from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from core.db_helper import db_helper
from domains.users import User

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_db(
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
) -> AsyncGenerator[SQLAlchemyUserDatabase]:
    """
    Dependency function to provide a SQLAlchemy user database instance.

    Args:
        session (AsyncSession): Injected SQLAlchemy async session.

    Yields:
        SQLAlchemyUserDatabase: The user database instance.
    """
    yield SQLAlchemyUserDatabase(session, User)
