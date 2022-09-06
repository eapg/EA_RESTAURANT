from src.constants import audit
from src.lib.entities import inventory


def build_inventory(inventory_id=None, entity_status=None, update_by=None):
    inventory_instance = inventory.Inventory()
    inventory_instance.id = inventory_id
    inventory_instance.entity_status = entity_status or audit.Status.ACTIVE
    inventory_instance.update_by = update_by or "create by test"
    return inventory_instance


def build_inventories(count=1):
    return [build_inventory(inventory_id=n) for n in range(count)]
