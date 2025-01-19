from datetime import date
from typing import List

from sqlalchemy import (
    String,
    Integer,
    Date,
)
from sqlalchemy.orm import mapped_column, Mapped, relationship

from models.base import Base
from models.mixins import IntIdPkMixin


class Queue(IntIdPkMixin, Base):
    __tablename__ = "queues"

    name: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )
    start_time: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )
    max_slots: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=30,
    )

    # по названию связи в связуемой таблице
    entries: Mapped[List["QueueEntries"]] = relationship(
        "QueueEntries",
        back_populates="queue",
    )
    queue_tags: Mapped[List["Tags"]] = relationship(
        "Tags",
        secondary="queue_tags",
        back_populates="queues",
    )



