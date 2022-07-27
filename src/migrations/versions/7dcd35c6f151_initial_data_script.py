"""initial_data_script

Revision ID: 7dcd35c6f151
Revises: f094737d0027
Create Date: 2022-07-27 14:32:23.753325

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7dcd35c6f151'
down_revision = 'f094737d0027'
branch_labels = None
depends_on = None


def upgrade():
    path = r"C:\Users\EpenaG\PycharmProjects\EA_RESTAURANT\src\scripts\seeder.sql"
    file = open(path, 'r')
    data_script = str(file.read())
    file.close()
    sql_text = sa.text(data_script)
    op.execute(sql_text)


def downgrade():
    pass
