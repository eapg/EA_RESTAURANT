"""refactor app refresh token table

Revision ID: 62e36e9c1bf1
Revises: 3b2f675ecb1d
Create Date: 2022-11-17 08:36:58.136817

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "62e36e9c1bf1"
down_revision = "3b2f675ecb1d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_constraint(
        "fk_refresh_tokens_app_clients", "app_refresh_tokens", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_refresh_tokens_users", "app_refresh_tokens", type_="foreignkey"
    )
    op.drop_column("app_refresh_tokens", "app_client_id")
    op.drop_column("app_refresh_tokens", "user_name")


def downgrade() -> None:
    pass
