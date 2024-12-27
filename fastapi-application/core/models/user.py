from typing import TYPE_CHECKING
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase

from .base import Base

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class User(SQLAlchemyBaseUserTableUUID, Base):

    @classmethod
    def get_db(cls,session:"AsyncSession"):
        return SQLAlchemyUserDatabase(session,User)