"""add movie_country_assoc model

Revision ID: 195838e2bbe3
Revises: a6c0f9a05182
Create Date: 2026-01-14 16:04:49.676884

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = "195838e2bbe3"
down_revision: Union[str, None] = "a6c0f9a05182"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "movie_country_associations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("country_id", sa.Integer(), nullable=False),
        sa.Column("movie_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["country_id"],
            ["countries.id"],
            name=op.f("fk_movie_country_associations_country_id_countries"),
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["movie_id"],
            ["movies.id"],
            name=op.f("fk_movie_country_associations_movie_id_movies"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "id", name=op.f("pk_movie_country_associations")
        ),
        sa.UniqueConstraint("country_id", "movie_id", name="uq_country_movie"),
    )


def downgrade() -> None:
    op.drop_table("movie_country_associations")
