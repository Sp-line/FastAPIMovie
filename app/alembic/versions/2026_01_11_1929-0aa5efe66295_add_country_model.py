"""add country model

Revision ID: 0aa5efe66295
Revises: 597cd780ff4c
Create Date: 2026-01-11 19:29:57.420443

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0aa5efe66295"
down_revision: Union[str, None] = "597cd780ff4c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "countrys",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("slug", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_countrys")),
        sa.UniqueConstraint("name", name=op.f("uq_countrys_name")),
        sa.UniqueConstraint("slug", name=op.f("uq_countrys_slug")),
    )


def downgrade() -> None:
    op.drop_table("countrys")
