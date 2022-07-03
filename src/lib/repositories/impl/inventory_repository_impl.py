# This file has the inventory repository
from datetime import datetime
from src.constants.audit import Status
from src.lib.repositories.inventory_repository import InventoryRepository


class InventoryRepositoryImpl(InventoryRepository):
    def __init__(self):
        self._inventories = {}
        self._current_id = 1

    def add(self, inventory):
        inventory.id = self._current_id
        inventory.create_date = datetime.now()
        inventory.update_by = inventory.create_by
        inventory.update_date = inventory.create_date
        self._inventories[inventory.id] = inventory
        self._current_id += 1

    def get_by_id(self, inventory_id):
        inventory_to_return = self._inventories[inventory_id]
        inventory_filtered = list(
            filter(
                lambda inventory: inventory.entity_status == Status.ACTIVE,
                [inventory_to_return],
            )
        )
        return inventory_filtered[0]

    def get_all(self):
        inventories = list(self._inventories.values())
        inventories_filtered = list(
            filter(
                lambda inventory: inventory.entity_status == Status.ACTIVE, inventories
            )
        )
        return list(inventories_filtered)

    def delete_by_id(self, inventory_id, inventory):
        inventory_to_be_delete = self.get_by_id(inventory_id)
        inventory_to_be_delete.entity_status = Status.DELETED
        inventory_to_be_delete.update_date = datetime.now()
        inventory_to_be_delete.update_by = inventory.update_by
        self._update_by_id(
            inventory_id, inventory_to_be_delete, use_merge_with_existing=False
        )

    def update_by_id(self, inventory_id, inventory):
        self._update_by_id(inventory_id, inventory)

    def _update_by_id(self, inventory_id, inventory, use_merge_with_existing=True):
        current_inventory = (
            self.get_by_id(inventory_id) if use_merge_with_existing else inventory
        )
        current_inventory.update_date = datetime.now()
        current_inventory.update_by = inventory.update_by or current_inventory.update_by
        current_inventory.entity_status = (
            inventory.entity_status or current_inventory.entity_status
        )

