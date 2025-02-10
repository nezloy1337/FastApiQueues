""" created table for queues

Revision ID: 429bc6b5c8a1
Revises: 7b8614aefb34
Create Date: 2025-01-01 19:12:17.927147

"""

from typing import Sequence, Union

import fastapi_users_db_sqlalchemy
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "429bc6b5c8a1"
down_revision: Union[str, None] = "7b8614aefb34"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        "queues",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=10), nullable=False),
        sa.Column("start_time", sa.Date(), nullable=False),
        sa.Column("max_slots", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_queues")),
    )
    op.create_table(
        "queue_entries",
        sa.Column("queue_id", sa.Integer(), nullable=False),
        sa.Column(
            "user_id",
            fastapi_users_db_sqlalchemy.generics.GUID(),
            nullable=False,
        ),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.CheckConstraint(
            "position BETWEEN 1 AND 30",
            name=op.f("ck_queue_entries_check_position_range"),
        ),
        sa.ForeignKeyConstraint(
            ["queue_id"],
            ["queues.id"],
            name=op.f("fk_queue_entries_queue_id_queues"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
            name=op.f("fk_queue_entries_user_id_user"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_queue_entries")),
        sa.UniqueConstraint("queue_id", "position", name="uq_queue_position"),
        sa.UniqueConstraint("queue_id", "user_id", name="uq_queue_user"),
    )


def downgrade() -> None:
    op.drop_table("queue_entries")
    op.drop_table("queues")
