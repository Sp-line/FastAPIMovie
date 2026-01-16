"""add check constraints to country

Revision ID: 8108e91f6f75
Revises: 195838e2bbe3
Create Date: 2026-01-16 16:23:47.550182

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

from constants import COUNTRY_NAME_MIN_LEN, COUNTRY_SLUG_MIN_LEN

revision: str = "8108e91f6f75"
down_revision: Union[str, None] = "195838e2bbe3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_check_constraint(
        "check_country_name_min_len",
        "countries",
        sa.text(f"char_length(name) >= {COUNTRY_NAME_MIN_LEN}")
    )
    op.create_check_constraint(
        "check_country_slug_min_len",
        "countries",
        sa.text(f"char_length(slug) >= {COUNTRY_SLUG_MIN_LEN}")
    )


def downgrade() -> None:
    op.drop_constraint("check_country_slug_min_len", "countries", type_="check")
    op.drop_constraint("check_country_name_min_len", "countries", type_="check")
