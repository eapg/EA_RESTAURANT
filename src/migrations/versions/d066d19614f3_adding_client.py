"""adding_client

Revision ID: d066d19614f3
Revises: 31387db2a03a
Create Date: 2022-07-28 09:45:42.057233

"""
from datetime import datetime

import sqlalchemy as sa
from alembic import op
from sqlalchemy.orm import Session

# revision identifiers, used by Alembic.
revision = "d066d19614f3"
down_revision = "31387db2a03a"
branch_labels = None
depends_on = None


def upgrade():

    op.execute(
        """
    INSERT INTO users(
      name,
      last_name,
      user_name,
      password,
      role,
      type,
      entity_status,
      created_by,
      created_date,
      updated_by,
      updated_date
      )
      
    VALUES(
      'Andres',
      'pena',
      'an_pe',
      '1234',
      'CLIENT',
      'EXTERNAL',
      'ACTIVE',
      1,
      CURRENT_TIMESTAMP,
      1,
      CURRENT_TIMESTAMP
      )   
    """
    )

    op.execute(
        """
    INSERT INTO clients(
      user_id,
      entity_status,
      created_by,
      created_date,
      updated_by,
      updated_date
      )

    VALUES(
      (select id
      from users
      where user_name = 'an_pe' and entity_status = 'ACTIVE'),
      'ACTIVE',
      1,
      CURRENT_TIMESTAMP,
      1,
      CURRENT_TIMESTAMP)
    """
    )

    op.execute(
        """
    UPDATE orders
        SET client_id = (SELECT id FROM clients LIMIT 1)
        WHERE client_id is NULL
    """
    )


def downgrade():

    op.execute(
        """
        UPDATE orders
            SET client_id = NULL
            WHERE client_id = (SELECT id FROM clients LIMIT 1)
        """
    )

    op.execute(
        """
        DELETE FROM clients
    """
    )

    op.execute(
        """
        DELETE FROM users
            WHERE user_name = 'an_pe'
    """
    )
