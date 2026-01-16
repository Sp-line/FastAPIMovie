"""add check constraints to persons

Revision ID: 908cb82f5b8b
Revises: 0f441058ac25
Create Date: 2026-01-16 16:55:17.459664

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

from constants import PERSON_FULL_NAME_MIN_LEN, PERSON_SLUG_MIN_LEN, ImageUrlLimits

revision: str = "908cb82f5b8b"
down_revision: Union[str, None] = "0f441058ac25"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_check_constraint(
        "check_person_full_name_min_len",
        "persons",
        sa.text(f"char_length(full_name) >= {PERSON_FULL_NAME_MIN_LEN}")
    )
    op.create_check_constraint(
        "check_person_slug_min_len",
        "persons",
        sa.text(f"char_length(slug) >= {PERSON_SLUG_MIN_LEN}")
    )
    op.create_check_constraint(
        "check_person_photo_url_not_empty",
        "persons",
        sa.text(f"char_length(photo_url) > {ImageUrlLimits.MIN}")
    )


def downgrade() -> None:
    op.drop_constraint("check_person_photo_url_not_empty", "persons", type_="check")
    op.drop_constraint("check_person_slug_min_len", "persons", type_="check")
    op.drop_constraint("check_person_full_name_min_len", "persons", type_="check")
