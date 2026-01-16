"""add check constraints to movie shots

Revision ID: 0f441058ac25
Revises: acba0521b71f
Create Date: 2026-01-16 16:40:27.820489

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

from constants import MOVIE_SHOT_CAPTION_URL_MIN_LEN, IMAGE_URL_MIN_LEN

revision: str = "0f441058ac25"
down_revision: Union[str, None] = "acba0521b71f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_check_constraint(
        "check_movie_shot_caption_min_len",
        "movie_shots",
        sa.text(f"char_length(caption) >= {MOVIE_SHOT_CAPTION_URL_MIN_LEN}")
    )
    op.create_check_constraint(
        "check_movie_shot_image_url_not_empty",
        "movie_shots",
        sa.text(f"char_length(image_url) > {IMAGE_URL_MIN_LEN}")
    )


def downgrade() -> None:
    op.drop_constraint("check_movie_shot_image_url_not_empty", "movie_shots", type_="check")
    op.drop_constraint("check_movie_shot_caption_min_len", "movie_shots", type_="check")
