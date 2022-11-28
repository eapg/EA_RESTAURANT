"""adding-grant type and app client id to refresh token table

Revision ID: 4c830869ce96
Revises: 62e36e9c1bf1
Create Date: 2022-11-28 08:56:58.310708

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4c830869ce96"
down_revision = "62e36e9c1bf1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("app_refresh_tokens", sa.Column("grant_type", sa.String(20)))
    op.add_column("app_refresh_tokens", sa.Column("app_client_id", sa.Integer()))
    op.create_foreign_key(
        "fk_refresh_token_client",
        "app_refresh_tokens",
        "clients",
        ["app_client_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_refresh_token_client", "app_refresh_tokens", type_="foreignkey"
    )
    op.drop_column("app_refresh_tokens", "grant_type")
    op.drop_column("app_refresh_tokens", "app_client_id")
