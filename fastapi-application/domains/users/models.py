from typing import TYPE_CHECKING, Any, List

import bson
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.base.model import Base

if TYPE_CHECKING:
    from domains.queues import QueueEntries


class User(SQLAlchemyBaseUserTableUUID, Base):

    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)

    queue_entries: Mapped[List["QueueEntries"]] = relationship(
        "QueueEntries", back_populates="user"
    )

    def model_dump(self) -> dict[str, Any]:

        return {
            "id": bson.Binary.from_uuid(self.id),
            "first_name": self.first_name,
            "last_name": self.last_name,
        }
