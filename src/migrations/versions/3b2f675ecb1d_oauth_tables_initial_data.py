""" oauth tables initial data

Revision ID: 3b2f675ecb1d
Revises: a7934568d9f0
Create Date: 2022-11-11 09:23:16.344319

"""
import os

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3b2f675ecb1d"
down_revision = "a7934568d9f0"
branch_labels = None
depends_on = None
dir_name = os.path.dirname(__file__)


def upgrade() -> None:

    path = os.path.join(
        dir_name, "..", "..", "scripts", "oauth_tables_initial_data.sql"
    )
    file = open(path, "r")
    data_script = str(file.read())
    file.close()
    sql_text = sa.text(data_script)
    op.execute(sql_text)


def downgrade() -> None:
    op.execute(f'TRUNCATE app_clients_scopes RESTART IDENTITY CASCADE;')
    op.execute(f'TRUNCATE app_clients RESTART IDENTITY CASCADE;')
    op.execute(f'TRUNCATE app_client_users RESTART IDENTITY CASCADE;')
