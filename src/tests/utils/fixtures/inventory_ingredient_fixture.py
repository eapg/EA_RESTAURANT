from src.lib.entities.inventory_ingredient import InventoryIngredient
from src.tests.utils.fixtures.ingredient_fixture import build_ingredient
from src.tests.utils.fixtures.inventory_fixture import build_inventory


def build_inventory_ingredient(
    inventory_ingredient_id=None, ingredient=None, inventory=None, ingredient_quantity=None
):
    inventory_ingredient = InventoryIngredient()
    inventory_ingredient.id = inventory_ingredient_id
    inventory_ingredient.inventory = inventory or build_inventory()
    inventory_ingredient.ingredient = ingredient or build_ingredient()
    inventory_ingredient.ingredient_quantity = ingredient_quantity or 1

    return inventory_ingredient


def build_inventory_ingredients(count=1):
    return [
        build_inventory_ingredient(
            ingredient=build_ingredient(ingredient_id=n),
            ingredient_quantity=n,
        )
        for n in range(count)
    ]
