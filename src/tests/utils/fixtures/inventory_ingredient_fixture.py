from src.constants.audit import Status
from src.lib.entities.inventory_ingredient import InventoryIngredient


def build_inventory_ingredient(
    inventory_ingredient_id=None,
    ingredient_id=None,
    inventory_id=None,
    ingredient_quantity=None,
    entity_status=None,
    create_by=None,
    update_by=None,
):
    inventory_ingredient = InventoryIngredient()
    inventory_ingredient.id = inventory_ingredient_id
    inventory_ingredient.inventory_id = inventory_id
    inventory_ingredient.ingredient_id = ingredient_id
    inventory_ingredient.ingredient_quantity = ingredient_quantity or 1
    inventory_ingredient.entity_status = entity_status or Status.ACTIVE
    inventory_ingredient.create_by = create_by
    inventory_ingredient.update_by = update_by

    return inventory_ingredient


def build_inventory_ingredients(count=1):
    return [
        build_inventory_ingredient(
            ingredient_id=n,
            ingredient_quantity=n,
        )
        for n in range(count)
    ]
