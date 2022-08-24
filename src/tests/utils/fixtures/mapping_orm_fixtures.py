from datetime import datetime

from src.constants.audit import Status
from src.lib.entities.sqlalchemy_orm_mapping import Chef, Product, Ingredient, Inventory


def build_chef(
    chef_id=None,
    user_id=None,
    name=None,
    skill=None,
    entity_status=None,
    create_by=None,
    update_by=None,
):

    chef = Chef()
    chef.id = chef_id
    chef.user_id = user_id or 1
    chef.name = name or "testing-chef"
    chef.skill = skill or 1
    chef.entity_status = entity_status or Status.ACTIVE.value
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

    product = Product()
    product.id = product_id or 1
    product.name = name or "testing-product"
    product.description = description or "description"
    product.entity_status = (entity_status or Status.ACTIVE.value,)
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

    ingredient = Ingredient()
    ingredient.id = ingredient_id or 1
    ingredient.name = name or "testing-ingredient"
    ingredient.description = description or "description"
    ingredient.entity_status = (entity_status or Status.ACTIVE.value,)
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

    inventory = Inventory()
    inventory.id = inventory_id or 1
    inventory.name = name or "testing-inventory"
    inventory.description = description or "description"
    inventory.entity_status = (entity_status or Status.ACTIVE.value,)
    inventory.created_by = create_by or 1
    inventory.created_date = create_date or datetime.now()
    inventory.updated_date = update_date or create_date
    inventory.updated_by = update_by or create_by

    return inventory


def build_inventories(count=1):
    return [build_inventory(name=f"testing-inventory{n}") for n in range(count)]
