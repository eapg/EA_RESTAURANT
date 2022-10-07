"""mongo-initial-data

Revision ID: da1fd865c698
Revises: e96d49093b33
Create Date: 2022-09-14 09:54:00.367087

"""
from alembic import op
import sqlalchemy as sa

revision = "da1fd865c698"
down_revision = "e96d49093b33"
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.add_column(
        "order_status_histories",
        sa.Column("mongo_order_status_history_uuid", sa.String()),
    )

    op.execute("TRUNCATE TABLE order_status_histories;")


def downgrade() -> None:
    pass
