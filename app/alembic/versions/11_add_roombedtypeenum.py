"""add roombedtypeenum

Revision ID: 11
Revises: 10
Create Date: 2026-06-14 21:23:32.635795

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "11"
down_revision: Union[str, Sequence[str], None] = "10"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    roombedtypeenum = postgresql.ENUM(
        "single",
        "double",
        "queen",
        "king",
        "twin",
        "sofa",
        "bunk",
        name="roombedtypeenum",
    )
    roombedtypeenum.create(op.get_bind(), checkfirst=True)

    op.alter_column(
        "room_types",
        "bed_type",
        existing_type=sa.VARCHAR(length=30),
        type_=sa.Enum(
            "single",
            "double",
            "queen",
            "king",
            "twin",
            "sofa",
            "bunk",
            name="roombedtypeenum",
        ),
        existing_nullable=False,
        postgresql_using="bed_type::text::roombedtypeenum",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "room_types",
        "bed_type",
        existing_type=sa.Enum(
            "single",
            "double",
            "queen",
            "king",
            "twin",
            "sofa",
            "bunk",
            name="roombedtypeenum",
        ),
        type_=sa.VARCHAR(length=30),
        existing_nullable=False,
    )

    op.execute("DROP TYPE IF EXISTS roombedtypeenum")
