# initial data to test the kitchen simulator

from src.constants.order_status import OrderStatus
from src.constants.cooking_type import CookingType
from src.core import ioc
from src.tests.utils.fixtures import (
    ingredient_fixture,
    inventory_fixture,
    inventory_ingredient_fixture,
    product_fixture,
    chef_fixture,
    order_detail_fixture,
    order_fixture,
    product_ingredient_fixture,
    order_detail_product_fixture,
)


instance_ioc = ioc.get_ioc_instance()
ingredient_controller = instance_ioc.get_instance("ingredient_controller")
product_ingredient_controller = instance_ioc.get_instance(
    "product_ingredient_controller"
)
inventory_ingredient_controller = instance_ioc.get_instance(
    "inventory_ingredient_controller"
)
inventory_controller = instance_ioc.get_instance("inventory_controller")
product_controller = instance_ioc.get_instance("product_controller")
chef_controller = instance_ioc.get_instance("chef_controller")
order_detail_product_controller = instance_ioc.get_instance(
    "order_detail_product_controller"
)
order_detail_controller = instance_ioc.get_instance("order_detail_controller")
order_controller = instance_ioc.get_instance("order_controller")
order_status_history_controller = instance_ioc.get_instance(
    "order_status_history_controller"
)


def create_inventory():

    inventory = inventory_fixture.build_inventory()
    inventory_controller.add(inventory)


def create_ingredients():
    ingredient_cheese = ingredient_fixture.build_ingredient(
        name="cheese", description="cheddar cheese", ingredient_type=CookingType.ADDING
    )
    ingredient_controller.add(ingredient_cheese)
    ingredient_bread = ingredient_fixture.build_ingredient(
        name="bread", description="italian bread", ingredient_type=CookingType.ROASTING
    )
    ingredient_controller.add(ingredient_bread)
    ingredient_tomato = ingredient_fixture.build_ingredient(
        name="tomato", description="roma tomato", ingredient_type=CookingType.ADDING
    )
    ingredient_controller.add(ingredient_tomato)
    ingredient_meat = ingredient_fixture.build_ingredient(
        name="meat", description="hamburger meat", ingredient_type=CookingType.FRYING
    )
    ingredient_controller.add(ingredient_meat)
    ingredient_bacon = ingredient_fixture.build_ingredient(
        name="bacon", description="bacon", ingredient_type=CookingType.ADDING
    )
    ingredient_controller.add(ingredient_bacon)


def create_inventory_ingredients():
    inventory_1 = inventory_controller.get_by_id(1)

    cheese = ingredient_controller.get_by_id(1)
    inventory_ingredient_cheese = (
        inventory_ingredient_fixture.build_inventory_ingredient(
            ingredient=cheese, ingredient_quantity=100, inventory=inventory_1
        )
    )
    inventory_ingredient_controller.add(inventory_ingredient_cheese)

    bread = ingredient_controller.get_by_id(2)
    inventory_ingredient_bread = (
        inventory_ingredient_fixture.build_inventory_ingredient(
            ingredient=bread, ingredient_quantity=100, inventory=inventory_1
        )
    )
    inventory_ingredient_controller.add(inventory_ingredient_bread)

    tomato = ingredient_controller.get_by_id(3)
    inventory_ingredient_tomato = (
        inventory_ingredient_fixture.build_inventory_ingredient(
            ingredient=tomato, ingredient_quantity=100, inventory=inventory_1
        )
    )
    inventory_ingredient_controller.add(inventory_ingredient_tomato)

    meat = ingredient_controller.get_by_id(4)
    inventory_ingredient_meat = inventory_ingredient_fixture.build_inventory_ingredient(
        ingredient=meat, ingredient_quantity=100, inventory=inventory_1
    )
    inventory_ingredient_controller.add(inventory_ingredient_meat)

    bacon = ingredient_controller.get_by_id(5)
    inventory_ingredient_bacon = (
        inventory_ingredient_fixture.build_inventory_ingredient(
            ingredient=bacon, ingredient_quantity=100, inventory=inventory_1
        )
    )
    inventory_ingredient_controller.add(inventory_ingredient_bacon)


def create_product():
    product_hamburger = product_fixture.build_product(
        name="hamburger", description="bacon cheese burger"
    )
    product_controller.add(product_hamburger)


def create_product_ingredients():
    # product hamburger
    product_1 = product_controller.get_by_id(1)
    # ingredients
    cheese = ingredient_controller.get_by_id(1)
    bread = ingredient_controller.get_by_id(2)
    tomato = ingredient_controller.get_by_id(3)
    meat = ingredient_controller.get_by_id(4)
    bacon = ingredient_controller.get_by_id(5)

    product_ingredient_cheese = product_ingredient_fixture.build_product_ingredient(
        product=product_1, ingredient=cheese, quantity=2
    )
    product_ingredient_controller.add(product_ingredient_cheese)

    product_ingredient_bread = product_ingredient_fixture.build_product_ingredient(
        product=product_1, ingredient=bread, quantity=2
    )
    product_ingredient_controller.add(product_ingredient_bread)

    product_ingredient_tomato = product_ingredient_fixture.build_product_ingredient(
        product=product_1, ingredient=tomato, quantity=2
    )
    product_ingredient_controller.add(product_ingredient_tomato)

    product_ingredient_meat = product_ingredient_fixture.build_product_ingredient(
        product=product_1, ingredient=meat, quantity=1
    )
    product_ingredient_controller.add(product_ingredient_meat)

    product_ingredient_bacon = product_ingredient_fixture.build_product_ingredient(
        product=product_1, ingredient=bacon, quantity=2
    )
    product_ingredient_controller.add(product_ingredient_bacon)


def create_order_details():
    order_detail_1 = order_detail_fixture.build_order_detail()
    order_detail_controller.add(order_detail_1)


def create_order_detail_product():

    product_1 = product_controller.get_by_id(1)
    order_detail_1 = order_detail_controller.get_by_id(1)
    order_detail_product = order_detail_product_fixture.build_order_detail_product(
        order_detail=order_detail_1, product=product_1, quantity=2
    )
    order_detail_product_controller.add(order_detail_product)


def create_order():
    order_detail_1 = order_detail_controller.get_by_id(1)
    order_1 = order_fixture.build_order(
        order_details=order_detail_1, status=OrderStatus.NEW_ORDER
    )
    order_controller.add(order_1)


def create_chefs():
    chef_principal = chef_fixture.build_chef(name="Elido p", chef_skills=5)
    chef_intermediate = chef_fixture.build_chef(name="Andres p", chef_skills=3)
    chef_basic = chef_fixture.build_chef(name="Juan p", chef_skills=1)

    chef_controller.add(chef_principal)
    chef_controller.add(chef_intermediate)
    chef_controller.add(chef_basic)


def run_initial_data():
    create_inventory()
    create_ingredients()
    create_inventory_ingredients()
    create_product()
    create_product_ingredients()
    create_order_details()
    create_order_detail_product()
    create_order()
    create_chefs()


if __name__ == "__main__":
    run_initial_data()
