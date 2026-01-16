"""add check constraints to movies

Revision ID: 2aa023a732c4
Revises: 908cb82f5b8b
Create Date: 2026-01-16 17:04:09.346588

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

from constants import ImageUrlLimits, MovieLimits

revision: str = "2aa023a732c4"
down_revision: Union[str, None] = "908cb82f5b8b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_check_constraint(
        "check_duration_limits",
        "movies",
        sa.text(f"duration >= {MovieLimits.DURATION_MIN} AND duration <= {MovieLimits.DURATION_MAX}")
    )
    op.create_check_constraint(
        "check_release_year_min",
        "movies",
        sa.text(f"release_year >= {MovieLimits.RELEASE_YEAR_MIN}")
    )
    op.create_check_constraint(
        "check_movie_title_not_empty",
        "movies",
        sa.text(f"char_length(title) > {MovieLimits.TITLE_MIN}")
    )
    op.create_check_constraint(
        "check_movie_slug_not_empty",
        "movies",
        sa.text(f"char_length(slug) > {MovieLimits.SLUG_MIN}")
    )
    op.create_check_constraint(
        "check_movie_poster_url_not_empty",
        "movies",
        sa.text(f"char_length(poster_url) > {ImageUrlLimits.MIN}")
    )
    op.create_check_constraint(
        "check_movie_age_rating_not_empty",
        "movies",
        sa.text(f"char_length(age_rating) > {MovieLimits.AGE_RATING_MIN}")
    )


def downgrade() -> None:
    op.drop_constraint("check_movie_age_rating_not_empty", "movies", type_="check")
    op.drop_constraint("check_movie_poster_url_not_empty", "movies", type_="check")
    op.drop_constraint("check_movie_slug_not_empty", "movies", type_="check")
    op.drop_constraint("check_movie_title_not_empty", "movies", type_="check")
    op.drop_constraint("check_release_year_min", "movies", type_="check")
    op.drop_constraint("check_duration_limits", "movies", type_="check")
