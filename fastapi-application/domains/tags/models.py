from typing import List

from sqlalchemy import (
    String,
)
from sqlalchemy.orm import mapped_column, Mapped, relationship

from core.base.mixins import IntIdPkMixin
from core.base.model import Base


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


