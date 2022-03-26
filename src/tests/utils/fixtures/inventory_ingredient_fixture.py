from src.lib.entities.inventory_ingredient import InventoryIngredient


def build_inventory_ingredient(inventory_ingredient_id=None, name=None, description=None):
    inventory_ingredient = InventoryIngredient()
    inventory_ingredient.id = inventory_ingredient_id
    inventory_ingredient.name = name or "testing-inventory_ingredient"
    inventory_ingredient.description = description or "testing-description"

    return inventory_ingredient


def build_inventory_ingredients(count=1):
    return [
        build_inventory_ingredient(
            name=f"testing-inventory_ingredient{n}", description=f"testing-description{n}"
        )
        for n in range(count)
    ]
