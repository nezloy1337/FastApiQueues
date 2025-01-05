"""added first and last names for user

Revision ID: 7b8614aefb34
Revises: 567f634f61a1
Create Date: 2024-12-29 20:45:42.156829

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7b8614aefb34"
down_revision: Union[str, None] = "567f634f61a1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("user", sa.Column("first_name", sa.String(), nullable=False))
    op.add_column("user", sa.Column("last_name", sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column("user", "last_name")
    op.drop_column("user", "first_name")

