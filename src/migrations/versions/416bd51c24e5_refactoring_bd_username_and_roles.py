"""refactoring-bd-username-and-roles

Revision ID: 416bd51c24e5
Revises: c26049706f23
Create Date: 2023-01-03 08:47:55.497499

"""
from alembic import op
import sqlalchemy as sa

from src.core.password_encoder_config import get_password_encoder

# revision identifiers, used by Alembic.
revision = "416bd51c24e5"
down_revision = "c26049706f23"
branch_labels = None
depends_on = None

SQL_QUERY_USER_DEFAULT_PROCEDURE = """
DROP PROCEDURE IF EXISTS insert_user_with_defaults;

CREATE PROCEDURE insert_user_with_defaults(
           user_name VARCHAR(50) DEFAULT 'elido',
      user_last_name VARCHAR(50) DEFAULT 'pena',
      user_username VARCHAR(50) DEFAULT 'test_user',
       user_password VARCHAR(500) DEFAULT '1234',
           user_roles user_role_enum DEFAULT 'SEEDER',
           user_type user_type_enum DEFAULT 'INTERNAL',
  user_entity_status status_enum DEFAULT 'ACTIVE',
      user_created_by BIGINT DEFAULT 1,
    user_created_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
      user_updated_by BIGINT DEFAULT 1,
    user_updated_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
)
LANGUAGE 'plpgsql' AS
$$
BEGIN
  INSERT INTO users
              (
                name,
                last_name,
                username,
                password,
                roles,
                type,
                entity_status,
                created_by,
                created_date,
                updated_by,
                updated_date
              )
       VALUES (
                user_name,
                user_last_name,
                user_username,
                user_password,
                user_roles,
                user_type,
                user_entity_status,
                user_created_by,
                user_created_date,
                user_updated_by,
                user_updated_date
              );
END;
$$;
"""


def upgrade() -> None:
    password_encoder = get_password_encoder()
    bd_user_encrypted_password = password_encoder.encode_password("1234abcd")

    op.alter_column("users", "role", new_column_name="roles", nullable=False)
    op.execute(sa.text(" ALTER TYPE user_role_enum ADD VALUE 'ADMINISTRATOR' "))
    op.execute(
        sa.text(" UPDATE app_clients_scopes SET scope = 'READ' where app_client_id = 1")
    )
    op.execute(
        sa.text(
            " UPDATE users SET password = :encrypted_password where id = 3"
        ).bindparams(encrypted_password=bd_user_encrypted_password)
    )
    op.execute(sa.text(SQL_QUERY_USER_DEFAULT_PROCEDURE))


def downgrade() -> None:
    op.alter_column("users", "roles", new_column_name="role", nullable=False)
