from datetime import datetime

from src.constants.audit import Status
from src.lib.entities.sqlalchemy_orm_mapping import Chef, Product


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
