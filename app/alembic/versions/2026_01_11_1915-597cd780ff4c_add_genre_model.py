"""add genre model

Revision ID: 597cd780ff4c
Revises: 
Create Date: 2026-01-11 19:15:43.095478

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "597cd780ff4c"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "genres",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("slug", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_genres")),
        sa.UniqueConstraint("name", name=op.f("uq_genres_name")),
        sa.UniqueConstraint("slug", name=op.f("uq_genres_slug")),
    )


def downgrade() -> None:
    op.drop_table("genres")
