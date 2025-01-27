"""tags table and queuetags table

Revision ID: 34d20a85ece6
Revises: 429bc6b5c8a1
Create Date: 2025-01-09 04:00:11.008402

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "34d20a85ece6"
down_revision: Union[str, None] = "429bc6b5c8a1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "tags",
        sa.Column("name", sa.String(length=15), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_tags")),
    )
    op.create_table(
        "queue_tags",
        sa.Column("queue_id", sa.Integer(), nullable=False),
        sa.Column("tag_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.ForeignKeyConstraint(
            ["queue_id"],
            ["queues.id"],
            name=op.f("fk_queue_tags_queue_id_queues"),
        ),
        sa.ForeignKeyConstraint(
            ["tag_id"], ["tags.id"], name=op.f("fk_queue_tags_tag_id_tags")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_queue_tags")),
    )


def downgrade() -> None:

    op.drop_table("queue_tags")
    op.drop_table("tags")
