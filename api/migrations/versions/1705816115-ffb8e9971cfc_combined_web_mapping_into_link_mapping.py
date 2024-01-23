"""
Combined web mapping into link mapping.

Revision ID: ffb8e9971cfc
Revises: 5f91f5cf93fe
Create Date: 2024-01-20 21:48:35.114513

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "ffb8e9971cfc"
down_revision = "5f91f5cf93fe"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("web_maps")
    op.add_column("link_maps", sa.Column("xpath", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("link_maps", "xpath")
    op.create_table(
        "web_maps",
        sa.Column("id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("server_id", sa.BIGINT(), autoincrement=False, nullable=False),
        sa.Column("user_id", sa.BIGINT(), autoincrement=False, nullable=False),
        sa.Column("created_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
        sa.Column("matches", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("xpath", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint("id", name="web_maps_pkey"),
    )
    # ### end Alembic commands ###