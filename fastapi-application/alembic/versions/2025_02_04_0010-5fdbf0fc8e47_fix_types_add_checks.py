"""fix types,add checks

Revision ID: 5fdbf0fc8e47
Revises: 01445204797c
Create Date: 2025-02-04 00:10:51.719067

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "5fdbf0fc8e47"
down_revision: Union[str, None] = "01445204797c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "queues",
        "start_time",
        existing_type=sa.DATE(),
        type_=sa.DateTime(),
        existing_nullable=False,
    )

    # added manually
    op.create_check_constraint(
        "check_position_number", "queues", "max_slots BETWEEN 1 AND 40"
    )

    # added manually
    op.create_check_constraint(
        "check_event_date", "queues", "start_time >= CURRENT_DATE"
    )


def downgrade() -> None:

    op.alter_column(
        "queues",
        "start_time",
        existing_type=sa.DateTime(),
        type_=sa.DATE(),
        existing_nullable=False,
    )
    op.drop_constraint(
        "check_position_number", "queues", type_="check"
    )  # added manually
    op.drop_constraint("check_event_date", "queues", type_="check")  # added manually
