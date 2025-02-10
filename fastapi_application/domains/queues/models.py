from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.base import Base
from core.base.mixins import IntIdPkMixin

if TYPE_CHECKING:
    from domains.tags import Tags
    from domains.users import User


class Queue(IntIdPkMixin, Base):
    """
    Represents a queue with a name, start time, and limited slots.

    Attributes:
        name (str): The name of the queue (max length: 10).
        start_time (datetime): The scheduled start time of the queue.
        max_slots (int): The maximum number of slots (default: 30).
        entries (List["QueueEntries"]): Related queue entries.
        queue_tags (List["Tags"]): Tags associated with the queue.
    """

    __tablename__ = "queues"

    name: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )
    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
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

    __table_args__ = (
        CheckConstraint(
            "max_slots BETWEEN 1 AND 40",
            name="check_position_number",
        ),
        CheckConstraint(
            "start_time >= CURRENT_DATE",
            name="check_event_date",
        ),
    )


class QueueEntries(IntIdPkMixin, Base):
    """
    Represents an entry in a queue, linking users to queue positions.

    Attributes:
        queue_id (int): Foreign key referencing the queue.
        user_id (str): Foreign key referencing the user.
        position (int): Position of the user in the queue.
        queue (Queue): Relationship to the queue.
        user (User): Relationship to the user.
    """

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


class QueueTags(IntIdPkMixin, Base):
    """
    Represents a link between a queue and a tag.

    Attributes:
        queue_id (int): Foreign key referencing the queue.
        tag_id (int): Foreign key referencing the tag.
    """

    __tablename__ = "queue_tags"

    queue_id: Mapped[int] = mapped_column(
        ForeignKey(
            "queues.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
    )

    tag_id: Mapped[int] = mapped_column(
        ForeignKey(
            "tags.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "queue_id",
            "tag_id",
            name="uq_username_email",
        ),
    )
