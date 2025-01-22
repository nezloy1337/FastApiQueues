from typing import TYPE_CHECKING, List

import bson
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.base.model import Base

if TYPE_CHECKING:
    from domains.queues import QueueEntries
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


    def model_dump(self):
        return {
            "id":bson.Binary.from_uuid(self.id), 
            "first_name":self.first_name,
            "last_name":self.last_name,
        }
