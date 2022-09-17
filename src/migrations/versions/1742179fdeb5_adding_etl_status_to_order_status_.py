"""adding etl status to order status history table

Revision ID: 1742179fdeb5
Revises: da1fd865c698
Create Date: 2022-09-16 22:34:50.000517

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1742179fdeb5'
down_revision = 'da1fd865c698'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("order_status_histories", sa.Column("etl_status", sa.String(length=50)))


def downgrade() -> None:
    pass
