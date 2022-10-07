"""alter order table

Revision ID: e96d49093b33
Revises: 3d244de0f7a2
Create Date: 2022-09-07 08:35:44.793146

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e96d49093b33"
down_revision = "3d244de0f7a2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column("orders", "assigned_chef_id", nullable=True)

    op.execute("Update orders SET assigned_chef_id = NULL")


def downgrade() -> None:
    pass
