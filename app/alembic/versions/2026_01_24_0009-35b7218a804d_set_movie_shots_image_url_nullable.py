"""set movie_shots image_url nullable

Revision ID: 35b7218a804d
Revises: 2aa023a732c4
Create Date: 2026-01-24 00:09:32.239571

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "35b7218a804d"
down_revision: Union[str, None] = "2aa023a732c4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "movie_shots",
        "image_url",
        existing_type=sa.VARCHAR(length=1024),
        nullable=True,
    )


def downgrade() -> None:
    op.alter_column(
        "movie_shots",
        "image_url",
        existing_type=sa.VARCHAR(length=1024),
        nullable=False,
    )
