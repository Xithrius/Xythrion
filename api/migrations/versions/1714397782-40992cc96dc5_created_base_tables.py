"""
Created base tables.

Revision ID: 40992cc96dc5
Revises:
Create Date: 2024-04-29 06:36:22.807688

"""

import sqlalchemy as sa
from alembic import op

revision = "40992cc96dc5"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "command_metrics",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("used_at", sa.DateTime(), nullable=False),
        sa.Column("command_name", sa.String(), nullable=False),
        sa.Column("successfully_completed", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("command_metrics_pkey")),
    )
    op.create_table(
        "link_map_channels",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("server_id", sa.BigInteger(), nullable=True),
        sa.Column("input_channel_id", sa.BigInteger(), nullable=True),
        sa.Column("output_channel_id", sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("link_map_channels_pkey")),
    )
    op.create_table(
        "link_map_converters",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("from_link", sa.String(), nullable=False),
        sa.Column("to_link", sa.String(), nullable=True),
        sa.Column("xpath", sa.String(), nullable=True),
        sa.CheckConstraint(
            "((to_link IS NOT NULL AND xpath IS NULL) OR (to_link IS NULL AND xpath IS NOT NULL))",
            name=op.f("link_map_converters_check_xor_constraint_check"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("link_map_converters_pkey")),
    )
    op.create_table(
        "pins",
        sa.Column("server_id", sa.BigInteger(), nullable=False),
        sa.Column("channel_id", sa.BigInteger(), nullable=False),
        sa.Column("message_id", sa.BigInteger(), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("server_id", "channel_id", "message_id", name=op.f("pins_pkey")),
    )
    op.create_table(
        "trusted",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("trusted_pkey")),
        sa.UniqueConstraint("user_id", name=op.f("trusted_user_id_key")),
    )
    op.create_table(
        "channel_converter_association",
        sa.Column("channel_id", sa.UUID(), nullable=False),
        sa.Column("converter_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["channel_id"],
            ["link_map_channels.id"],
            name=op.f("channel_converter_association_channel_id_fkey"),
        ),
        sa.ForeignKeyConstraint(
            ["converter_id"],
            ["link_map_converters.id"],
            name=op.f("channel_converter_association_converter_id_fkey"),
        ),
        sa.PrimaryKeyConstraint("channel_id", "converter_id", name=op.f("channel_converter_association_pkey")),
    )


def downgrade() -> None:
    op.drop_table("channel_converter_association")
    op.drop_table("trusted")
    op.drop_table("pins")
    op.drop_table("link_map_converters")
    op.drop_table("link_map_channels")
    op.drop_table("command_metrics")
