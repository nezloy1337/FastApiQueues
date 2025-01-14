from typing import List

from sqlalchemy import (
    String,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import mapped_column, Mapped, relationship

from core.models.mixins import IntIdPkMixin
from core.models.postgresql.base import Base


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


class QueueTags(IntIdPkMixin, Base):
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
