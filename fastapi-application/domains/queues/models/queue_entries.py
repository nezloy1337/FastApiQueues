
from sqlalchemy import (
    Integer,
    ForeignKey,
    UniqueConstraint,
    CheckConstraint,
)
from sqlalchemy.orm import mapped_column, Mapped, relationship

from domains.queues.models.queue import Queue
from models.base import Base
from models.mixins import IntIdPkMixin


class QueueEntries(IntIdPkMixin, Base):
    __tablename__ = "queue_entries"

    queue_id: Mapped[int] = mapped_column(
        ForeignKey(
            "queues.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
    )
    user_id: Mapped[str] = mapped_column(
        ForeignKey(
            "user.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
    )
    position: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    queue: Mapped[Queue] = relationship(
        "Queue",
        back_populates="entries",
    )
    user: Mapped["User"] = relationship(
        "User",
        back_populates="queue_entries",
    )

    __table_args__ = (
        UniqueConstraint(
            "queue_id",
            "position",
            name="uq_queue_position",
        ),
        UniqueConstraint(
            "queue_id",
            "user_id",
            name="uq_queue_user",
        ),
        CheckConstraint(
            "position BETWEEN 1 AND 30",
            name="check_position_range",
        ),
    )