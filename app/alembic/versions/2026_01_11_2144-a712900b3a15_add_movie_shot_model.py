"""add movie_shot model

Revision ID: a712900b3a15
Revises: f52c5801c77c
Create Date: 2026-01-11 21:44:09.542852

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a712900b3a15"
down_revision: Union[str, None] = "f52c5801c77c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "movie_shots",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("image_url", sa.String(length=1024), nullable=False),
        sa.Column("caption", sa.String(length=255), nullable=False),
        sa.Column("movie_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["movie_id"],
            ["movies.id"],
            name=op.f("fk_movie_shots_movie_id_movies"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_movie_shots")),
    )


def downgrade() -> None:
    op.drop_table("movie_shots")
