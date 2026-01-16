"""add check constraints to genres

Revision ID: acba0521b71f
Revises: 8108e91f6f75
Create Date: 2026-01-16 16:35:13.102653

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

from constants.genre import GENRE_NAME_MIN_LEN, GENRE_SLUG_MIN_LEN

revision: str = "acba0521b71f"
down_revision: Union[str, None] = "8108e91f6f75"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_check_constraint(
        "check_genre_name_min_len",
        "genres",
        sa.text(f"char_length(name) >= {GENRE_NAME_MIN_LEN}")
    )
    op.create_check_constraint(
        "check_genre_slug_min_len",
        "genres",
        sa.text(f"char_length(slug) >= {GENRE_SLUG_MIN_LEN}")
    )


def downgrade() -> None:
    op.drop_constraint("check_genre_slug_min_len", "genres", type_="check")
    op.drop_constraint("check_genre_name_min_len", "genres", type_="check")
