"""use AgeRating enum for age_rating field in Movie model

Revision ID: 9543b1b0f337
Revises: 35b7218a804d
Create Date: 2026-02-13 22:48:38.934495

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "9543b1b0f337"
down_revision: Union[str, None] = "35b7218a804d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


CONSTRAINT_NAME = "check_movie_age_rating_not_empty"
TABLE_NAME = "movies"

enum_type = postgresql.ENUM("G", "PG", "PG-13", "R", "NC-17", name="age_rating")

def upgrade() -> None:
    op.drop_constraint(CONSTRAINT_NAME, TABLE_NAME, type_="check")

    enum_type.create(op.get_bind())
    op.alter_column(
        "movies",
        "age_rating",
        existing_type=sa.VARCHAR(length=10),
        type_=sa.Enum("G", "PG", "PG-13", "R", "NC-17", name="age_rating"),
        existing_nullable=True,
        postgresql_using="age_rating::age_rating"
    )


def downgrade() -> None:
    op.alter_column(
        "movies",
        "age_rating",
        existing_type=sa.Enum(
            "G", "PG", "PG-13", "R", "NC-17", name="age_rating"
        ),
        type_=sa.VARCHAR(length=10),
        existing_nullable=True,
    )
    enum_type.drop(op.get_bind())

    op.create_check_constraint(
        CONSTRAINT_NAME,
        TABLE_NAME,
        "char_length(age_rating) > 2"
    )
