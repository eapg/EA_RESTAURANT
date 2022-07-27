"""db_script

Revision ID: c5d3236b81a3
Revises: 
Create Date: 2022-07-27 09:05:34.676045

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c5d3236b81a3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    path = r"C:\Users\EpenaG\PycharmProjects\EA_RESTAURANT\src\scripts\db_script.sql"
    file = open(path, 'r')
    data_script = str(file.read())
    file.close()
    sql_text = sa.text(data_script)
    op.execute(sql_text)


def downgrade():
    pass
