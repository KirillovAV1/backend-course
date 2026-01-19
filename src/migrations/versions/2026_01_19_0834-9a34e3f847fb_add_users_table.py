"""add users table

Revision ID: 9a34e3f847fb
Revises: d84ad0296070
Create Date: 2026-01-19 08:34:25.309517

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9a34e3f847fb"
down_revision: Union[str, Sequence[str], None] = "d84ad0296070"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("hashed_password", sa.String(length=100), nullable=False),
        sa.Column("phone_number", sa.String(length=20), nullable=True),
        sa.Column("first_name", sa.String(length=15), nullable=True),
        sa.Column("last_name", sa.String(length=15), nullable=True),
        sa.Column("username", sa.String(length=20), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
