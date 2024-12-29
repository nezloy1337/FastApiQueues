from typing import TYPE_CHECKING
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy import String

from .base import Base

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class User(SQLAlchemyBaseUserTableUUID, Base):

    first_name: Mapped[str] = mapped_column(String,nullable=False)
    last_name: Mapped[str] = mapped_column(String,nullable=False)

    @classmethod
    def get_db(cls,session:"AsyncSession"):
        return SQLAlchemyUserDatabase(session,User)