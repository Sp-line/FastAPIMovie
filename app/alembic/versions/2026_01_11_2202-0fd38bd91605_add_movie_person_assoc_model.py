"""add movie_person_assoc model

Revision ID: 0fd38bd91605
Revises: a712900b3a15
Create Date: 2026-01-11 22:02:11.842221

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0fd38bd91605"
down_revision: Union[str, None] = "a712900b3a15"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "movie_person_associations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("movie_id", sa.Integer(), nullable=False),
        sa.Column("person_id", sa.Integer(), nullable=False),
        sa.Column(
            "role",
            sa.Enum(
                "ACTOR", "DIRECTOR", "WRITER", "PRODUCER", name="movieroletype"
            ),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["movie_id"],
            ["movies.id"],
            name=op.f("fk_movie_person_associations_movie_id_movies"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["person_id"],
            ["persons.id"],
            name=op.f("fk_movie_person_associations_person_id_persons"),
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint(
            "id", name=op.f("pk_movie_person_associations")
        ),
        sa.UniqueConstraint(
            "person_id", "movie_id", "role", name="uq_movie_person_role"
        ),
    )


def downgrade() -> None:
    op.drop_table("movie_person_associations")
