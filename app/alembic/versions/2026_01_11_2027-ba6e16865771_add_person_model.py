"""add person model

Revision ID: ba6e16865771
Revises: 0aa5efe66295
Create Date: 2026-01-11 20:27:56.190418

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "ba6e16865771"
down_revision: Union[str, None] = "0aa5efe66295"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "persons",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("full_name", sa.String(length=150), nullable=False),
        sa.Column("slug", sa.String(length=150), nullable=False),
        sa.Column("photo_url", sa.String(length=1024), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_persons")),
        sa.UniqueConstraint("slug", name=op.f("uq_persons_slug")),
    )


def downgrade() -> None:
    op.drop_table("persons")
