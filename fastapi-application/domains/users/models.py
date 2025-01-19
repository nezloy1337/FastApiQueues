from typing import TYPE_CHECKING, List

from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.base.model import Base

if TYPE_CHECKING:
    from models import QueueEntries
    from sqlalchemy.ext.asyncio import AsyncSession


class User(SQLAlchemyBaseUserTableUUID, Base):

    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)

    queue_entries: Mapped[List["QueueEntries"]] = relationship(
        "QueueEntries", back_populates="user"
    )

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, User)
