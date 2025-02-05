from typing import TYPE_CHECKING, Any, List

import bson
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.base.model import Base

if TYPE_CHECKING:
    from domains.queues import QueueEntries


class User(SQLAlchemyBaseUserTableUUID, Base):
    """
    Represents a user in the system.

    Attributes:
        first_name (str): The user's first name.
        last_name (str): The user's last name.
        queue_entries (List[QueueEntries]): The user's queue entries.
    """

    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)

    queue_entries: Mapped[List["QueueEntries"]] = relationship(
        "QueueEntries", back_populates="user"
    )

    def model_dump(self) -> dict[str, Any]:
        """
        Serializes the user object to a dictionary format.

        Returns:
            dict[str, Any]: A dictionary representation of the user.
        """

        return {
            "id": bson.Binary.from_uuid(self.id),
            "first_name": self.first_name,
            "last_name": self.last_name,
        }
