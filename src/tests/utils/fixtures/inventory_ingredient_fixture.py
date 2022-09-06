from src.constants import audit
from src.lib.entities import inventory_ingredient


def build_inventory_ingredient(
    inventory_ingredient_id=None,
    ingredient_id=None,
    inventory_id=None,
    ingredient_quantity=None,
    entity_status=None,
    create_by=None,
    update_by=None,
):
    inventory_ingredient_instance = inventory_ingredient.InventoryIngredient()
    inventory_ingredient_instance.id = inventory_ingredient_id
    inventory_ingredient_instance.inventory_id = inventory_id
    inventory_ingredient_instance.ingredient_id = ingredient_id
    inventory_ingredient_instance.quantity = ingredient_quantity or 1
    inventory_ingredient_instance.entity_status = entity_status or audit.Status.ACTIVE
    inventory_ingredient_instance.create_by = create_by
    inventory_ingredient_instance.update_by = update_by

    return inventory_ingredient_instance


def build_inventory_ingredients(count=1):
    return [
        build_inventory_ingredient(
            ingredient_id=n,
            ingredient_quantity=n,
        )
        for n in range(count)
    ]
