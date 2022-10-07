"""client_table

Revision ID: 31387db2a03a
Revises: 7dcd35c6f151
Create Date: 2022-07-27 15:02:30.642109

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "31387db2a03a"
down_revision = "7dcd35c6f151"
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        "clients",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column(
            "entity_status",
            postgresql.ENUM("ACTIVE", "DELETE", name="status_enum", create_type=False),
            nullable=False,
        ),
        sa.Column("created_by", sa.Integer(), nullable=False),
        sa.Column("created_date", sa.DateTime),
        sa.Column("updated_by", sa.Integer(), nullable=False),
        sa.Column("updated_date", sa.DateTime),
        sa.PrimaryKeyConstraint("id"),
    )

    op.add_column("orders", sa.Column("client_id", sa.Integer()))


def downgrade():

    op.drop_column("orders", "client_id")
    op.drop_table("clients")
