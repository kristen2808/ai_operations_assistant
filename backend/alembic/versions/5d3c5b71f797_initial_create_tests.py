"""initial create tests

Revision ID: 5d3c5b71f797
Revises: 
Create Date: 2026-10-21 18:03:43.625636

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5d3c5b71f797'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "tests",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("jmeno", sa.String(length=100), nullable=False),
        sa.Column("prijmeni", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("tests")
