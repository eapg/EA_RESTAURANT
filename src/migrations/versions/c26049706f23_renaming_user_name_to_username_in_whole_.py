"""renaming user_name to username in whole project

Revision ID: c26049706f23
Revises: 4c830869ce96
Create Date: 2022-11-28 16:31:41.230984

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c26049706f23'
down_revision = '4c830869ce96'
branch_labels = None
depends_on = None

SQL_QUERY_TO_CREATE_USER_STORE_PROCEDURES_WITH_USERNAME = """
CREATE PROCEDURE insert_user_with_defaults(
           user_name VARCHAR(50) DEFAULT 'elido',
      user_last_name VARCHAR(50) DEFAULT 'pena',
      user_username VARCHAR(50) DEFAULT 'test_user',
       user_password VARCHAR(500) DEFAULT '1234',
           user_role user_role_enum DEFAULT 'SEEDER',
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
                role,
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
                user_role,
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
SQL_QUERY_TO_CREATE_USER_STORE_PROCEDURES_WITH_USER_NAME = """
CREATE PROCEDURE insert_user_with_defaults(
           user_name VARCHAR(50) DEFAULT 'elido',
      user_last_name VARCHAR(50) DEFAULT 'pena',
      user_user_name VARCHAR(50) DEFAULT 'test_user',
       user_password VARCHAR(500) DEFAULT '1234',
           user_role user_role_enum DEFAULT 'SEEDER',
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
       VALUES (
                user_name,
                user_last_name,
                user_user_name,
                user_password,
                user_role,
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
    op.alter_column("users", "user_name", new_column_name="username")
    op.alter_column("app_client_users", "user_name", new_column_name="username")
    op.execute(sa.text('DROP PROCEDURE IF EXISTS insert_user_with_defaults;'))
    op.execute(sa.text(SQL_QUERY_TO_CREATE_USER_STORE_PROCEDURES_WITH_USERNAME))


def downgrade() -> None:
    op.execute(sa.text('DROP PROCEDURE IF EXISTS insert_user_with_defaults;'))
    op.execute(sa.text(SQL_QUERY_TO_CREATE_USER_STORE_PROCEDURES_WITH_USER_NAME))
    op.alter_column("users", "username", new_column_name="user_name")
    op.alter_column("app_client_users", "username", new_column_name="user_name")
