"""adding python app client

Revision ID: 8dda351079cc
Revises: 809dd14b4b64
Create Date: 2023-05-08 14:26:54.689568

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8dda351079cc"
down_revision = "809dd14b4b64"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
    INSERT INTO app_clients(
      client_name,
      client_id,
      client_secret,
      access_token_expiration_time,
      refresh_token_expiration_time,
      entity_status,
      created_by,
      created_date,
      updated_by,
      updated_date
      )
    
    VALUES(
      'python',
      'python_client_001',
      'cHl0aG9uX3NlY3JldF8wMDE=',
      600,
      1200,
      'ACTIVE',
      1,
      CURRENT_TIMESTAMP,
      1,
      CURRENT_TIMESTAMP    
      )
        """
    )


def downgrade() -> None:
    op.execute(
        """
    DELETE FROM app_clients
           WHERE client_id = 'python_client_001'
        """
    )
