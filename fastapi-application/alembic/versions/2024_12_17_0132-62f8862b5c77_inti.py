"""inti

Revision ID: 62f8862b5c77
Revises: 
Create Date: 2024-12-17 01:32:34.729410

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "62f8862b5c77"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "curr_histories",
        sa.Column("USD", sa.Float(), nullable=False),
        sa.Column("EUR", sa.Float(), nullable=False),
        sa.Column("JPY", sa.Float(), nullable=False),
        sa.Column("GBP", sa.Float(), nullable=False),
        sa.Column("AUD", sa.Float(), nullable=False),
        sa.Column("CAD", sa.Float(), nullable=False),
        sa.Column("CHF", sa.Float(), nullable=False),
        sa.Column("CNY", sa.Float(), nullable=False),
        sa.Column("SEK", sa.Float(), nullable=False),
        sa.Column("NZD", sa.Float(), nullable=False),
        sa.Column("BYN", sa.Float(), nullable=False),
        sa.Column("DATE", sa.DateTime(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_curr_histories")),
    )



def downgrade() -> None:
    op.drop_table("curr_histories")

