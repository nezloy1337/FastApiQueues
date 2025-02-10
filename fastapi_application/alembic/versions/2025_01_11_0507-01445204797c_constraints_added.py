"""constraints added 

Revision ID: 01445204797c
Revises: 34d20a85ece6
Create Date: 2025-01-11 05:07:46.254631

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "01445204797c"
down_revision: Union[str, None] = "34d20a85ece6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.drop_constraint(
        "fk_queue_entries_queue_id_queues", "queue_entries", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_queue_entries_user_id_user", "queue_entries", type_="foreignkey"
    )
    op.create_foreign_key(
        op.f("fk_queue_entries_user_id_user"),
        "queue_entries",
        "user",
        ["user_id"],
        ["id"],
        onupdate="CASCADE",
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        op.f("fk_queue_entries_queue_id_queues"),
        "queue_entries",
        "queues",
        ["queue_id"],
        ["id"],
        onupdate="CASCADE",
        ondelete="CASCADE",
    )
    op.create_unique_constraint(
        "uq_username_email", "queue_tags", ["queue_id", "tag_id"]
    )
    op.drop_constraint("fk_queue_tags_tag_id_tags", "queue_tags", type_="foreignkey")
    op.drop_constraint(
        "fk_queue_tags_queue_id_queues", "queue_tags", type_="foreignkey"
    )
    op.create_foreign_key(
        op.f("fk_queue_tags_queue_id_queues"),
        "queue_tags",
        "queues",
        ["queue_id"],
        ["id"],
        onupdate="CASCADE",
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        op.f("fk_queue_tags_tag_id_tags"),
        "queue_tags",
        "tags",
        ["tag_id"],
        ["id"],
        onupdate="CASCADE",
        ondelete="CASCADE",
    )
    op.create_unique_constraint(op.f("uq_tags_name"), "tags", ["name"])


def downgrade() -> None:
    op.drop_constraint(op.f("uq_tags_name"), "tags", type_="unique")
    op.drop_constraint(
        op.f("fk_queue_tags_tag_id_tags"), "queue_tags", type_="foreignkey"
    )
    op.drop_constraint(
        op.f("fk_queue_tags_queue_id_queues"), "queue_tags", type_="foreignkey"
    )
    op.create_foreign_key(
        "fk_queue_tags_queue_id_queues",
        "queue_tags",
        "queues",
        ["queue_id"],
        ["id"],
    )
    op.create_foreign_key(
        "fk_queue_tags_tag_id_tags", "queue_tags", "tags", ["tag_id"], ["id"]
    )
    op.drop_constraint("uq_username_email", "queue_tags", type_="unique")
    op.drop_constraint(
        op.f("fk_queue_entries_queue_id_queues"),
        "queue_entries",
        type_="foreignkey",
    )
    op.drop_constraint(
        op.f("fk_queue_entries_user_id_user"),
        "queue_entries",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "fk_queue_entries_user_id_user",
        "queue_entries",
        "user",
        ["user_id"],
        ["id"],
    )
    op.create_foreign_key(
        "fk_queue_entries_queue_id_queues",
        "queue_entries",
        "queues",
        ["queue_id"],
        ["id"],
    )
