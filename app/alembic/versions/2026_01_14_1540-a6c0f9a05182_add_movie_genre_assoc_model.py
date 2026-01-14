"""add movie_genre_assoc model

Revision ID: a6c0f9a05182
Revises: 0fd38bd91605
Create Date: 2026-01-14 15:40:42.473612

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a6c0f9a05182"
down_revision: Union[str, None] = "0fd38bd91605"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "movie_genre_associations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("movie_id", sa.Integer(), nullable=False),
        sa.Column("genre_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["genre_id"],
            ["genres.id"],
            name=op.f("fk_movie_genre_associations_genre_id_genres"),
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["movie_id"],
            ["movies.id"],
            name=op.f("fk_movie_genre_associations_movie_id_movies"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "id", name=op.f("pk_movie_genre_associations")
        ),
        sa.UniqueConstraint("movie_id", "genre_id", name="uq_movie_genre"),
    )


def downgrade() -> None:
    op.drop_table("movie_genre_associations")
