"""oauth tables script

Revision ID: a7934568d9f0
Revises: 1742179fdeb5
Create Date: 2022-11-09 10:03:01.724285

"""
import os

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "a7934568d9f0"
down_revision = "1742179fdeb5"
branch_labels = None
depends_on = None
dir_name = os.path.dirname(__file__)


def upgrade() -> None:

    # alter users table to set user_name as unique
    op.create_unique_constraint("uq_user_name", "users", ["user_name"])

    # creating oath tables
    path = os.path.join(dir_name, "..", "..", "scripts", "oauth_tables_script.sql")
    file = open(path, "r")
    data_script = str(file.read())
    file.close()
    sql_text = sa.text(data_script)
    op.execute(sql_text)


def downgrade() -> None:
    op.drop_constraint("uq_user_name", "users")

    op.drop_constraint("fk_client_users_users", "app_client_users", type_="foreignkey")

    op.drop_constraint(
        "fk_clients_scopes_app_clients", "app_clients_scopes", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_client_users_app_clients", "app_client_users", type_="foreignkey"
    )

    op.drop_constraint(
        "fk_refresh_tokens_users", "app_refresh_tokens", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_refresh_tokens_app_clients", "app_refresh_tokens", type_="foreignkey"
    )

    op.drop_constraint(
        "fk_access_token_refresh_token", "app_access_tokens", type_="foreignkey"
    )

    op.drop_table("app_clients")
    op.drop_table("app_clients_scopes")
    op.drop_table("app_client_users")
    op.drop_table("app_access_tokens")
    op.drop_table("app_refresh_tokens")
