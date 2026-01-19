"""Email unique col

Revision ID: 3b31100a71dc
Revises: 9a34e3f847fb
Create Date: 2026-01-19 09:48:02.251237

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3b31100a71dc"
down_revision: Union[str, Sequence[str], None] = "9a34e3f847fb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "users", type_="unique")
