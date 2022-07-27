"""procedures_script

Revision ID: f094737d0027
Revises: c5d3236b81a3
Create Date: 2022-07-27 14:11:56.384396

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f094737d0027'
down_revision = 'c5d3236b81a3'
branch_labels = None
depends_on = None


def upgrade():
    path = r"C:\Users\EpenaG\PycharmProjects\EA_RESTAURANT\src\scripts\fixtures_script.sql"
    file = open(path, 'r')
    data_script = str(file.read())
    file.close()
    sql_text = sa.text(data_script)
    op.execute(sql_text)


def downgrade():
    pass
