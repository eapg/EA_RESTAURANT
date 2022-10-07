from src.constants.audit import Status
from src.lib.entities.inventory import Inventory


def build_inventory(inventory_id=None, entity_status=None, update_by=None):
    inventory = Inventory()
    inventory.id = inventory_id
    inventory.entity_status = entity_status or Status.ACTIVE
    inventory.update_by = update_by or "create by test"
    return inventory


def build_inventories(count=1):
    return [build_inventory(inventory_id=n) for n in range(count)]
