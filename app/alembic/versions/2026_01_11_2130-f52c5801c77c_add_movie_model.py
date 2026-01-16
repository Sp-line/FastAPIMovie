"""add movie model

Revision ID: f52c5801c77c
Revises: ba6e16865771
Create Date: 2026-01-11 21:30:52.763106

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "f52c5801c77c"
down_revision: Union[str, None] = "ba6e16865771"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "movies",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("slug", sa.String(length=255), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("duration", sa.SmallInteger(), nullable=False),
        sa.Column("age_rating", sa.String(length=10), nullable=True),
        sa.Column("premiere_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("release_year", sa.SmallInteger(), nullable=False),
        sa.Column("poster_url", sa.String(length=1024), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_movies")),
        sa.UniqueConstraint("slug", name=op.f("uq_movies_slug")),
    )


def downgrade() -> None:
    op.drop_table("movies")
