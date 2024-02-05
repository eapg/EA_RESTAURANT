from datetime import datetime

from sqlalchemy import text

from src.constants.audit import Status
from src.constants.cooking_type import CookingType
from src.constants.oauth2 import Roles, GranTypes
from src.constants.order_status import OrderStatus
from src.core.password_encoder_config import get_password_encoder
from src.lib.entities.sqlalchemy_orm_mapping import (
    Chef,
    Ingredient,
    Inventory,
    InventoryIngredient,
    Order,
    OrderDetail,
    OrderStatusHistory,
    Product,
    ProductIngredient,
)
from src.tests.utils.fixtures.fixture_args import BaseEntityArgs
from src.utils.sql_oath2_queries import (
    SQL_QUERY_TO_ADD_ACCESS_TOKEN,
    SQL_QUERY_TO_ADD_REFRESH_TOKEN,
)

DEFAULT_BASE_ENTITY_ARGS = BaseEntityArgs()


def build_chef(
    chef_id=None,
    user_id=None,
    name=None,
    skill=None,
    fixture_args=DEFAULT_BASE_ENTITY_ARGS,
):

    chef = Chef()
    chef.id = chef_id
    chef.user_id = user_id or 1
    chef.name = name or "testing-chef"
    chef.skill = skill or 1
    chef.entity_status = fixture_args.entity_status or Status.ACTIVE.value
    chef.created_by = fixture_args.created_by or 1
    chef.updated_by = fixture_args.updated_by or None

    return chef


def build_chefs(count=1):
    return [
        build_chef(name=f"testing-chef{n}", skill=n, chef_id=n) for n in range(count)
    ]


def build_product(
    product_id=None, name=None, description=None, fixture_args=DEFAULT_BASE_ENTITY_ARGS
):

    product = Product()
    product.id = product_id or 1
    product.name = name or "testing-product"
    product.description = description or "description"
    product.entity_status = fixture_args.entity_status or Status.ACTIVE.value
    product.created_by = fixture_args.created_by or 1
    product.created_date = fixture_args.created_date or datetime.now()
    product.updated_date = fixture_args.updated_date or None
    product.updated_by = fixture_args.updated_by or None

    return product


def build_products(count=1):
    return [build_product(name=f"testing-product{n}") for n in range(count)]


def build_ingredient(
    ingredient_id=None,
    name=None,
    description=None,
    fixture_args=DEFAULT_BASE_ENTITY_ARGS,
):

    ingredient = Ingredient()
    ingredient.id = ingredient_id or 1
    ingredient.name = name or "testing-ingredient"
    ingredient.description = description or "description"
    ingredient.entity_status = (fixture_args.entity_status or Status.ACTIVE.value,)
    ingredient.created_by = fixture_args.created_by or 1
    ingredient.created_date = fixture_args.created_date or datetime.now()
    ingredient.updated_date = fixture_args.updated_date or None
    ingredient.updated_by = fixture_args.updated_by or None

    return ingredient


def build_ingredients(count=1):
    return [build_ingredient(name=f"testing-ingredient{n}") for n in range(count)]


def build_inventory(
    inventory_id=None,
    name=None,
    description=None,
    fixture_args=DEFAULT_BASE_ENTITY_ARGS,
):

    inventory = Inventory()
    inventory.id = inventory_id or 1
    inventory.name = name or "testing-inventory"
    inventory.description = description or "description"
    inventory.entity_status = (fixture_args.entity_status or Status.ACTIVE.value,)
    inventory.created_by = fixture_args.created_by or 1
    inventory.created_date = fixture_args.created_date or datetime.now()
    inventory.updated_date = fixture_args.updated_date
    inventory.updated_by = fixture_args.updated_by

    return inventory


def build_inventories(count=1):
    return [build_inventory(name=f"testing-inventory{n}") for n in range(count)]


def build_order_detail(
    order_detail_id=None,
    order_id=None,
    product_id=None,
    quantity=None,
    fixture_args=DEFAULT_BASE_ENTITY_ARGS,
):

    order_detail = OrderDetail()
    order_detail.id = order_detail_id or 1
    order_detail.order_id = order_id or 1
    order_detail.product_id = product_id or 1
    order_detail.quantity = quantity or 5
    order_detail.entity_status = fixture_args.entity_status or Status.ACTIVE
    order_detail.created_by = fixture_args.created_by or 1
    order_detail.created_date = fixture_args.created_date
    order_detail.updated_by = fixture_args.updated_by
    order_detail.updated_date = fixture_args.updated_date

    return order_detail


def build_order_details(count=1):
    return [build_order_detail(order_detail_id=n) for n in range(count)]


def build_product_ingredient(
    product_ingredient_id=None,
    product_id=None,
    ingredient_id=None,
    quantity=None,
    fixture_args=DEFAULT_BASE_ENTITY_ARGS,
):

    product_ingredient = ProductIngredient()
    product_ingredient.id = product_ingredient_id or 1
    product_ingredient.product_id = product_id or 1
    product_ingredient.ingredient_id = ingredient_id or 1
    product_ingredient.quantity = quantity or 5
    product_ingredient.cooking_type = CookingType.ADDING.value

    product_ingredient.entity_status = fixture_args.entity_status or Status.ACTIVE.value
    product_ingredient.created_by = fixture_args.created_by or 1
    product_ingredient.updated_by = fixture_args.updated_by

    return product_ingredient


def build_product_ingredients(count=1):
    return [build_product_ingredient(product_ingredient_id=n) for n in range(count)]


def build_inventory_ingredient(
    inventory_ingredient_id=None,
    ingredient_id=None,
    inventory_id=None,
    quantity=None,
    fixture_args=DEFAULT_BASE_ENTITY_ARGS,
):

    inventory_ingredient = InventoryIngredient()
    inventory_ingredient.id = inventory_ingredient_id or 1
    inventory_ingredient.ingredient_id = ingredient_id or 1
    inventory_ingredient.inventory_id = inventory_id or 1
    inventory_ingredient.quantity = quantity or 1
    inventory_ingredient.entity_status = (
        fixture_args.entity_status or Status.ACTIVE.value
    )
    inventory_ingredient.created_by = fixture_args.created_by or 1
    inventory_ingredient.updated_by = fixture_args.updated_by

    return inventory_ingredient


def build_inventory_ingredients(count=1):
    return [build_inventory_ingredient(inventory_ingredient_id=n) for n in range(count)]


def build_order_status_history(
    order_status_id=None,
    order_id=None,
    from_time=None,
    from_status=None,
    fixture_args=DEFAULT_BASE_ENTITY_ARGS,
):

    order_status_history = OrderStatusHistory()
    order_status_history.id = order_status_id or 1
    order_status_history.order_id = order_id or 1
    order_status_history.from_status = from_status
    order_status_history.to_status = OrderStatus.NEW_ORDER.name
    order_status_history.from_time = from_time
    order_status_history.to_time = datetime.now()
    order_status_history.entity_status = (
        fixture_args.entity_status or Status.ACTIVE.value
    )
    order_status_history.created_by = fixture_args.created_by or 1
    order_status_history.updated_by = fixture_args.updated_by

    return order_status_history


def build_order_status_histories(count=1):
    return [build_order_status_history(order_status_id=n) for n in range(count)]


def build_order(
    order_id=None,
    status=None,
    assigned_chef_id=None,
    client_id=None,
    fixture_args=DEFAULT_BASE_ENTITY_ARGS,
):

    order = Order()
    order.id = order_id or 1
    order.status = status or OrderStatus.NEW_ORDER.name
    order.assigned_chef_id = assigned_chef_id or 1
    order.client_id = client_id or 1
    order.entity_status = fixture_args.entity_status or Status.ACTIVE.value
    order.created_by = fixture_args.created_by or 1
    order.updated_by = fixture_args.updated_by or order.created_by

    return order


def build_orders(count=1):
    return [build_order(order_id=n) for n in range(count)]


def create_order_with_procedure(engine, assigned_chef_id=None, order_status=None):
    with engine.begin() as conn:
        conn.execute(
            text(
                """CALL insert_order_with_defaults(
                     order_assigned_chef_id:= :assigned_chef_id, 
                       order_status:= :order_status);"""
            ),
            {"assigned_chef_id": assigned_chef_id, "order_status": order_status},
        )


def create_order_detail_with_procedure(engine, order_id=None, product_id=None):
    with engine.begin() as conn:
        conn.execute(
            text(
                """CALL insert_order_detail_with_defaults(
                     order_detail_order_id:= :order_id, 
                       order_detail_product_id:= :product_id);"""
            ),
            {"order_id": order_id, "product_id": product_id},
        )


def create_product_ingredient_with_procedure(engine, product_id=None):
    with engine.begin() as conn:
        conn.execute(
            text(
                """CALL insert_product_ingredient_with_defaults(
                     product_ingredient_product_id:= :product_id);"""
            ),
            {"product_id": product_id},
        )


def create_user_with_procedure(
    engine, user_name=None, username=None, password=None, roles=None
):
    password_encoder = get_password_encoder()
    encrypted_password = password_encoder.encode_password(password)
    with engine.begin() as conn:
        conn.execute(
            text(
                """CALL insert_user_with_defaults(
                     user_name:= :user_name,
                     user_username:= :username,
                     user_password:= :password,
                     user_roles:= :roles);"""
            ),
            {
                "user_name": user_name,
                "username": username,
                "password": encrypted_password,
                "roles": roles or Roles.CHEF.value,
            },
        )


def insert_access_and_refresh_token_in_db(engine, access_token, refresh_token):

    with engine.begin() as conn:
        conn.execute(
            text(SQL_QUERY_TO_ADD_ACCESS_TOKEN),
            {"refresh_token_id": 1, "token": access_token},
        )

        conn.execute(
            text(SQL_QUERY_TO_ADD_REFRESH_TOKEN),
            {
                "token": refresh_token,
                "app_client_id": 1,
                "grant_type": GranTypes.CLIENT_CREDENTIALS.value,
            },
        )
