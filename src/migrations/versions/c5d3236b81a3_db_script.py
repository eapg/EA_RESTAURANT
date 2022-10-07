"""db_script

Revision ID: c5d3236b81a3
Revises: 
Create Date: 2022-07-27 09:05:34.676045

"""
import sqlalchemy as sa
from alembic import op
import os

# revision identifiers, used by Alembic.
revision = "c5d3236b81a3"
down_revision = None
branch_labels = None
depends_on = None
dir_name = os.path.dirname(__file__)


def upgrade():
    path = os.path.join(dir_name, '..', '..', 'scripts', 'db_script.sql')
    file = open(path, "r")
    data_script = str(file.read())
    file.close()
    sql_text = sa.text(data_script)
    op.execute(sql_text)


def downgrade():
    pass
