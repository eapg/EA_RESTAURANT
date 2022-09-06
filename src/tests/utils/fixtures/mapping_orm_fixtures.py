from datetime import datetime

from src.constants import audit
from src.constants import cooking_type
from src.constants import order_status
from src.lib.entities import sqlalchemy_orm_mapping


def build_chef(
    chef_id=None,
    user_id=None,
    name=None,
    skill=None,
    entity_status=None,
    create_by=None,
    update_by=None,
):

    chef = sqlalchemy_orm_mapping.Chef()
    chef.id = chef_id
    chef.user_id = user_id or 1
    chef.name = name or "testing-chef"
    chef.skill = skill or 1
    chef.entity_status = entity_status or audit.Status.ACTIVE.value
    chef.created_by = create_by or 1
    chef.updated_by = update_by or create_by

    return chef


def build_chefs(count=1):
    return [
        build_chef(name=f"testing-chef{n}", skill=n, chef_id=n) for n in range(count)
    ]


def build_product(
    product_id=None,
    name=None,
    description=None,
    entity_status=None,
    create_by=None,
    create_date=None,
    update_date=None,
    update_by=None,
):

    product = sqlalchemy_orm_mapping.Product()
    product.id = product_id or 1
    product.name = name or "testing-product"
    product.description = description or "description"
    product.entity_status = (entity_status or audit.Status.ACTIVE.value,)
    product.created_by = create_by or 1
    product.created_date = create_date or datetime.now()
    product.updated_date = update_date or create_date
    product.updated_by = update_by or create_by

    return product


def build_products(count=1):
    return [build_product(name=f"testing-product{n}") for n in range(count)]


def build_ingredient(
    ingredient_id=None,
    name=None,
    description=None,
    entity_status=None,
    create_by=None,
    create_date=None,
    update_date=None,
    update_by=None,
):

    ingredient = sqlalchemy_orm_mapping.Ingredient()
    ingredient.id = ingredient_id or 1
    ingredient.name = name or "testing-ingredient"
    ingredient.description = description or "description"
    ingredient.entity_status = (entity_status or audit.Status.ACTIVE.value,)
    ingredient.created_by = create_by or 1
    ingredient.created_date = create_date or datetime.now()
    ingredient.updated_date = update_date or create_date
    ingredient.updated_by = update_by or create_by

    return ingredient


def build_ingredients(count=1):
    return [build_ingredient(name=f"testing-ingredient{n}") for n in range(count)]


def build_inventory(
    inventory_id=None,
    name=None,
    description=None,
    entity_status=None,
    create_by=None,
    create_date=None,
    update_date=None,
    update_by=None,
):

    inventory = sqlalchemy_orm_mapping.Inventory()
    inventory.id = inventory_id or 1
    inventory.name = name or "testing-inventory"
    inventory.description = description or "description"
    inventory.entity_status = (entity_status or audit.Status.ACTIVE.value,)
    inventory.created_by = create_by or 1
    inventory.created_date = create_date or datetime.now()
    inventory.updated_date = update_date or create_date
    inventory.updated_by = update_by or create_by

    return inventory


def build_inventories(count=1):
    return [build_inventory(name=f"testing-inventory{n}") for n in range(count)]


def build_order_detail(
    order_detail_id=None,
    order_id=None,
    product_id=None,
    quantity=None,
    entity_status=None,
    create_by=None,
    update_by=None,
):

    order_detail = sqlalchemy_orm_mapping.OrderDetail()
    order_detail.id = order_detail_id or 1
    order_detail.order_id = order_id or 1
    order_detail.product_id = product_id or 1
    order_detail.quantity = quantity or 5
    order_detail.entity_status = entity_status or audit.Status.ACTIVE
    order_detail.created_by = create_by or 1
    order_detail.updated_by = update_by or create_by

    return order_detail


def build_order_details(count=1):
    return [build_order_detail(order_detail_id=n) for n in range(count)]


def build_product_ingredient(
    product_ingredient_id=None,
    product_id=None,
    ingredient_id=None,
    quantity=None,
    product_ingredient_cooking_type=None,
    entity_status=None,
    create_by=None,
    update_by=None,
):

    product_ingredient = sqlalchemy_orm_mapping.ProductIngredient()
    product_ingredient.id = product_ingredient_id or 1
    product_ingredient.product_id = product_id or 1
    product_ingredient.ingredient_id = ingredient_id or 1
    product_ingredient.quantity = quantity or 5
    product_ingredient.cooking_type = (
        product_ingredient_cooking_type or cooking_type.CookingType.ADDING.value
    )
    product_ingredient.entity_status = entity_status or audit.Status.ACTIVE.value
    product_ingredient.created_by = create_by or 1
    product_ingredient.updated_by = update_by or create_by

    return product_ingredient


def build_product_ingredients(count=1):
    return [build_product_ingredient(product_ingredient_id=n) for n in range(count)]


def build_inventory_ingredient(
    inventory_ingredient_id=None,
    ingredient_id=None,
    inventory_id=None,
    quantity=None,
    entity_status=None,
    create_by=None,
    update_by=None,
):

    inventory_ingredient = sqlalchemy_orm_mapping.InventoryIngredient()
    inventory_ingredient.id = inventory_ingredient_id or 1
    inventory_ingredient.ingredient_id = ingredient_id or 1
    inventory_ingredient.inventory_id = inventory_id or 1
    inventory_ingredient.quantity = quantity or 1
    inventory_ingredient.entity_status = entity_status or audit.Status.ACTIVE.value
    inventory_ingredient.created_by = create_by or 1
    inventory_ingredient.updated_by = update_by or create_by

    return inventory_ingredient


def build_inventory_ingredients(count=1):
    return [build_inventory_ingredient(inventory_ingredient_id=n) for n in range(count)]


def build_order_status_history(
    order_status_id=None,
    order_id=None,
    from_time=None,
    to_time=None,
    from_status=None,
    to_status=None,
    entity_status=None,
    create_by=None,
    update_by=None,
):

    order_status_history = sqlalchemy_orm_mapping.OrderStatusHistory()
    order_status_history.id = order_status_id or 1
    order_status_history.order_id = order_id or 1
    order_status_history.from_status = from_status
    order_status_history.to_status = (
        to_status or order_status.OrderStatus.NEW_ORDER.name
    )
    order_status_history.from_time = from_time
    order_status_history.to_time = to_time or datetime.now()
    order_status_history.entity_status = entity_status or audit.Status.ACTIVE.value
    order_status_history.created_by = create_by or 1
    order_status_history.updated_by = update_by or create_by

    return order_status_history


def build_order_status_histories(count=1):
    return [build_order_status_history(order_status_id=n) for n in range(count)]


def build_order(
    order_id=None,
    status=None,
    assigned_chef_id=None,
    client_id=None,
    entity_status=None,
    create_by=None,
    update_by=None,
):

    order = sqlalchemy_orm_mapping.Order()
    order.id = order_id or 1
    order.status = status or order_status.OrderStatus.NEW_ORDER.name
    order.assigned_chef_id = assigned_chef_id or 1
    order.client_id = client_id or 1
    order.entity_status = entity_status or audit.Status.ACTIVE.value
    order.created_by = create_by or 1
    order.updated_by = update_by or order.created_by

    return order


def build_orders(count=1):
    return [build_order(order_id=n) for n in range(count)]
