"""
Dropped command metric table.

Revision ID: 2c4eb0418e4d
Revises: 40992cc96dc5
Create Date: 2024-05-11 00:28:51.125962

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "2c4eb0418e4d"
down_revision = "40992cc96dc5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_table("command_metrics")


def downgrade() -> None:
    op.create_table(
        "command_metrics",
        sa.Column("id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column("used_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
        sa.Column("command_name", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("successfully_completed", sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint("id", name="command_metrics_pkey"),
    )
