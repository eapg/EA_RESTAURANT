"""initial_data_script

Revision ID: 7dcd35c6f151
Revises: f094737d0027
Create Date: 2022-07-27 14:32:23.753325

"""
import sqlalchemy as sa
from alembic import op
import os

# revision identifiers, used by Alembic.
revision = "7dcd35c6f151"
down_revision = "f094737d0027"
branch_labels = None
depends_on = None
dir_name = os.path.dirname(__file__)


def upgrade():
    path = os.path.join(dir_name, '..', '..', 'scripts', 'seeder.sql')
    file = open(path, "r")
    data_script = str(file.read())
    file.close()
    sql_text = sa.text(data_script)
    op.execute(sql_text)


def downgrade():
    pass
