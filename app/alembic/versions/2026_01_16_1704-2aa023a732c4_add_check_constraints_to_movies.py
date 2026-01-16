"""add check constraints to movies

Revision ID: 2aa023a732c4
Revises: 908cb82f5b8b
Create Date: 2026-01-16 17:04:09.346588

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

from constants import MOVIE_DURATION_MIN_VALUE, MOVIE_DURATION_MAX_VALUE, MOVIE_RELEASE_YEAR_MIN_VALUE, \
    MOVIE_TITLE_MIN_LEN, MOVIE_SLUG_MIN_LEN, IMAGE_URL_MIN_LEN, MOVIE_AGE_RATING_MIN_LEN


revision: str = "2aa023a732c4"
down_revision: Union[str, None] = "908cb82f5b8b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_check_constraint(
        "check_duration_limits",
        "movies",
        sa.text(f"duration >= {MOVIE_DURATION_MIN_VALUE} AND duration <= {MOVIE_DURATION_MAX_VALUE}")
    )
    op.create_check_constraint(
        "check_release_year_min",
        "movies",
        sa.text(f"release_year >= {MOVIE_RELEASE_YEAR_MIN_VALUE}")
    )
    op.create_check_constraint(
        "check_movie_title_not_empty",
        "movies",
        sa.text(f"char_length(title) > {MOVIE_TITLE_MIN_LEN}")
    )
    op.create_check_constraint(
        "check_movie_slug_not_empty",
        "movies",
        sa.text(f"char_length(slug) > {MOVIE_SLUG_MIN_LEN}")
    )
    op.create_check_constraint(
        "check_movie_poster_url_not_empty",
        "movies",
        sa.text(f"char_length(poster_url) > {IMAGE_URL_MIN_LEN}")
    )
    op.create_check_constraint(
        "check_movie_age_rating_not_empty",
        "movies",
        sa.text(f"char_length(age_rating) > {MOVIE_AGE_RATING_MIN_LEN}")
    )


def downgrade() -> None:
    op.drop_constraint("check_movie_age_rating_not_empty", "movies", type_="check")
    op.drop_constraint("check_movie_poster_url_not_empty", "movies", type_="check")
    op.drop_constraint("check_movie_slug_not_empty", "movies", type_="check")
    op.drop_constraint("check_movie_title_not_empty", "movies", type_="check")
    op.drop_constraint("check_release_year_min", "movies", type_="check")
    op.drop_constraint("check_duration_limits", "movies", type_="check")
