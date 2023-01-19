"""bd enums to varchar

Revision ID: 809dd14b4b64
Revises: 416bd51c24e5
Create Date: 2023-01-19 09:04:18.507062

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "809dd14b4b64"
down_revision = "416bd51c24e5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Changing entity status column from enum to varchar(20)
    op.execute(
        "ALTER TABLE app_client_users ALTER COLUMN entity_status TYPE varchar (20);"
    )
    op.execute("ALTER TABLE app_clients ALTER COLUMN entity_status TYPE varchar (20);")
    op.execute(
        "ALTER TABLE app_clients_scopes ALTER COLUMN entity_status TYPE varchar (20);"
    )
    op.execute("ALTER TABLE chefs ALTER COLUMN entity_status TYPE varchar (20);")
    op.execute("ALTER TABLE clients ALTER COLUMN entity_status TYPE varchar (20);")
    op.execute("ALTER TABLE ingredients ALTER COLUMN entity_status TYPE varchar (20);")
    op.execute("ALTER TABLE inventories ALTER COLUMN entity_status TYPE varchar (20);")
    op.execute(
        "ALTER TABLE inventory_ingredients ALTER COLUMN entity_status TYPE varchar (20);"
    )
    op.execute(
        "ALTER TABLE order_details ALTER COLUMN entity_status TYPE varchar (20);"
    )
    op.execute(
        "ALTER TABLE order_status_histories ALTER COLUMN entity_status TYPE varchar (20);"
    )
    op.execute("ALTER TABLE orders ALTER COLUMN entity_status TYPE varchar (20);")
    op.execute(
        "ALTER TABLE product_ingredients ALTER COLUMN entity_status TYPE varchar (20);"
    )
    op.execute("ALTER TABLE products ALTER COLUMN entity_status TYPE varchar (20);")
    op.execute("ALTER TABLE users ALTER COLUMN entity_status TYPE varchar (20);")

    # Changing cooking type column from enum to varchar(20)
    op.execute(
        "ALTER TABLE product_ingredients ALTER COLUMN cooking_type TYPE varchar (20);"
    )

    # Changing status type column from enum to varchar(20)
    op.execute("ALTER TABLE orders ALTER COLUMN status TYPE varchar (20);")

    # Changing scope type column from enum to varchar(100)
    op.execute("ALTER TABLE app_clients_scopes ALTER COLUMN scope TYPE varchar (100);")

    # Changing roles type column from enum to varchar(100)
    op.execute("ALTER TABLE users ALTER COLUMN roles TYPE varchar (100);")

    # Changing user_type type column from enum to varchar(20)
    op.execute("ALTER TABLE users ALTER COLUMN type TYPE varchar (20);")

    # Changing from_status/to_status type column from enum to varchar(20)
    op.execute(
        "ALTER TABLE order_status_histories ALTER COLUMN from_status TYPE varchar (20);"
    )
    op.execute(
        "ALTER TABLE order_status_histories ALTER COLUMN to_status TYPE varchar (20);"
    )

    op.execute("DROP TYPE IF EXISTS status_enum CASCADE;")
    op.execute("DROP TYPE IF EXISTS user_type_enum CASCADE;")
    op.execute("DROP TYPE IF EXISTS user_role_enum CASCADE;")
    op.execute("DROP TYPE IF EXISTS cooking_type_enum CASCADE;")
    op.execute("DROP TYPE IF EXISTS order_status_enum CASCADE;")
    op.execute("DROP TYPE IF EXISTS scope_enum CASCADE;")


def downgrade() -> None:
    op.execute("CREATE TYPE status_enum AS ENUM ('ACTIVE', 'DELETE');")
    op.execute("CREATE TYPE user_type_enum AS ENUM ('INTERNAL','EXTERNAL');")
    op.execute(
        "CREATE TYPE user_role_enum AS ENUM ('CHEF', 'CLIENT', 'CASHIER', 'SEEDER', 'KITCHEN_SIMULATOR');"
    )
    op.execute(
        "CREATE TYPE cooking_type_enum AS ENUM ('ADDING', 'ROASTING', 'BOILING', 'BAKING', 'FRYING', 'HEADING', "
        "'PREPARING_DRINK'); "
    )
    op.execute(
        "CREATE TYPE order_status_enum AS ENUM ('NEW_ORDER', 'IN_PROCESS', 'COMPLETED', 'CANCELLED');"
    )
    op.execute("CREATE TYPE scope_enum AS ENUM ('READ', 'WRITE');")

    op.execute(
        "ALTER TABLE app_client_users ALTER COLUMN entity_status TYPE status_enum USING entity_status::status_enum;"
    )
    op.execute(
        "ALTER TABLE app_clients ALTER COLUMN entity_status TYPE status_enum USING entity_status::status_enum;"
    )
    op.execute(
        "ALTER TABLE app_clients_scopes ALTER COLUMN entity_status TYPE status_enum USING entity_status::status_enum;"
    )
    op.execute(
        "ALTER TABLE chefs ALTER COLUMN entity_status TYPE status_enum USING entity_status::status_enum;"
    )
    op.execute(
        "ALTER TABLE clients ALTER COLUMN entity_status TYPE status_enum USING entity_status::status_enum;"
    )
    op.execute(
        "ALTER TABLE ingredients ALTER COLUMN entity_status TYPE status_enum USING entity_status::status_enum;"
    )
    op.execute(
        "ALTER TABLE inventories ALTER COLUMN entity_status TYPE status_enum USING entity_status::status_enum;"
    )
    op.execute(
        "ALTER TABLE inventory_ingredients ALTER COLUMN entity_status TYPE status_enum USING "
        "entity_status::status_enum; "
    )
    op.execute(
        "ALTER TABLE order_details ALTER COLUMN entity_status TYPE status_enum USING entity_status::status_enum;"
    )
    op.execute(
        "ALTER TABLE order_status_histories ALTER COLUMN entity_status TYPE status_enum USING "
        "entity_status::status_enum; "
    )
    op.execute(
        "ALTER TABLE orders ALTER COLUMN entity_status TYPE status_enum USING entity_status::status_enum;"
    )
    op.execute(
        "ALTER TABLE product_ingredients ALTER COLUMN entity_status TYPE status_enum USING entity_status::status_enum;"
    )
    op.execute(
        "ALTER TABLE products ALTER COLUMN entity_status TYPE status_enum USING entity_status::status_enum;"
    )
    op.execute(
        "ALTER TABLE users ALTER COLUMN entity_status TYPE status_enum USING entity_status::status_enum;"
    )

    op.execute(
        "ALTER TABLE product_ingredients ALTER COLUMN cooking_type TYPE cooking_type_enum USING "
        "cooking_type::cooking_type_enum; "
    )

    op.execute(
        "ALTER TABLE orders ALTER COLUMN status TYPE order_status_enum  USING status::order_status_enum;"
    )

    op.execute(
        "ALTER TABLE app_clients_scopes ALTER COLUMN scope TYPE scope_enum USING scope::scope_enum;"
    )

    op.execute(
        "ALTER TABLE users ALTER COLUMN roles TYPE user_role_enum USING roles::user_role_enum;"
    )

    op.execute(
        "ALTER TABLE users ALTER COLUMN type TYPE user_type_enum USING type::user_type_enum;"
    )

    op.execute(
        "ALTER TABLE order_status_histories ALTER COLUMN from_status TYPE order_status_enum USING "
        "from_status::order_status_enum; "
    )
    op.execute(
        "ALTER TABLE order_status_histories ALTER COLUMN to_status TYPE order_status_enum USING "
        "to_status::order_status_enum; "
    )
