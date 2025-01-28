from typing import TYPE_CHECKING, List

from sqlalchemy import (
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.base.mixins import IntIdPkMixin
from core.base.model import Base

if TYPE_CHECKING:
    from domains.queues import Queue


class Tags(IntIdPkMixin, Base):
    __tablename__ = "tags"

    name: Mapped[str] = mapped_column(
        String(15),
        nullable=False,
        unique=True,
    )

    queues: Mapped[List["Queue"]] = relationship(
        "Queue",
        secondary="queue_tags",
        back_populates="queue_tags",
    )
