from datetime import datetime, date
from typing import List

from sqlalchemy import (
    String,
    DateTime,
    Integer,
    ForeignKey,
    UniqueConstraint,
    CheckConstraint,
    Date,
)
from sqlalchemy.orm import mapped_column, Mapped, relationship
from core.models.mixins import IntIdPkMixin

from core.models.user import User
from core.models.base import Base

class Queue(IntIdPkMixin, Base):
    __tablename__ = "queues"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(10), nullable=False)
    start_time: Mapped[date] = mapped_column(Date, nullable=False)
    max_slots: Mapped[int] = mapped_column(Integer, nullable=False, default=30)

    entries:Mapped[List["QueueEntries"]] = relationship("QueueEntries", back_populates="queue")


class QueueEntries(IntIdPkMixin, Base):
    __tablename__ = "queue_entries"

    queue_id: Mapped[int] = mapped_column(ForeignKey("queues.id"), nullable=False)
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"), nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False)

    queue: Mapped[Queue] = relationship("Queue", back_populates="entries")
    user:Mapped["User"] = relationship("User", back_populates="queue_entries")

    __table_args__ = (
        UniqueConstraint("queue_id", "position", name="uq_queue_position"),
        UniqueConstraint("queue_id", "user_id", name="uq_queue_user"),
        CheckConstraint("position BETWEEN 1 AND 30", name="check_position_range"),
    )
