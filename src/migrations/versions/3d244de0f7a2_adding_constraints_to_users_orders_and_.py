"""adding constraints to users, orders and clients tables

Revision ID: 3d244de0f7a2
Revises: d066d19614f3
Create Date: 2022-07-28 16:20:05.126959

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "3d244de0f7a2"
down_revision = "d066d19614f3"
branch_labels = None
depends_on = None


def upgrade():
    op.create_foreign_key("fk_client_user", "clients", "users", ["user_id"], ["id"])
    op.create_foreign_key(
        "fk_client_user_created", "clients", "users", ["created_by"], ["id"]
    )
    op.create_foreign_key(
        "fk_client_user_updated", "clients", "users", ["updated_by"], ["id"]
    )
    op.create_foreign_key("fk_order_client", "orders", "clients", ["client_id"], ["id"])
    op.alter_column("orders", "client_id", nullable=False)


def downgrade():
    op.drop_constraint("fk_client_user", "clients", type_="foreignkey")
    op.drop_constraint("fk_client_user_created", "clients", type_="foreignkey")
    op.drop_constraint("fk_client_user_updated", "clients", type_="foreignkey")
    op.drop_constraint("fk_order_client", "orders", type_="foreignkey")
    op.alter_column("orders", "client_id", nullable=True)
