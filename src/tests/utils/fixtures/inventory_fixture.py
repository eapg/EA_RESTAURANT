from src.lib.entities.inventory import Inventory


def build_inventory(inventory_id=None, inventory_ingredients=None):
    inventory = Inventory()
    inventory.id = inventory_id
    inventory.inventory_ingredients = inventory_ingredients or []
    return inventory


def build_inventories(count=1):
    return [
        build_inventory(inventory_id=n, inventory_ingredients=[]) for n in range(count)
    ]
