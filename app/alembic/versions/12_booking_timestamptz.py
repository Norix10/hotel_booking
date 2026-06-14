"""Convert booking timestamps to timestamptz

Revision ID: 12
Revises: 11
Create Date: 2026-06-14 21:45:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "12"
down_revision: Union[str, Sequence[str], None] = "11"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "bookings",
        "check_in",
        existing_type=sa.DateTime(),
        type_=postgresql.TIMESTAMP(timezone=True),
        existing_nullable=False,
        postgresql_using="check_in AT TIME ZONE 'UTC'",
    )
    op.alter_column(
        "bookings",
        "check_out",
        existing_type=sa.DateTime(),
        type_=postgresql.TIMESTAMP(timezone=True),
        existing_nullable=False,
        postgresql_using="check_out AT TIME ZONE 'UTC'",
    )


def downgrade() -> None:
    op.alter_column(
        "bookings",
        "check_in",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        type_=sa.DateTime(),
        existing_nullable=False,
    )
    op.alter_column(
        "bookings",
        "check_out",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        type_=sa.DateTime(),
        existing_nullable=False,
    )
