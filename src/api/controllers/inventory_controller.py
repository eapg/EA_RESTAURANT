class InventoryController:
    def __init__(self, inventory_repository):
        self._inventory_repository = inventory_repository  # inventoryRepository

    def add(self, inventory):
        self._inventory_repository.add(inventory)

    def get_by_id(self, inventory_id):
        return self._inventory_repository.get_by_id(inventory_id)

    def get_all(self):
        return self._inventory_repository.get_all()

    def delete_by_id(self, inventory_id):
        self._inventory_repository.delete_by_id(inventory_id)

    def update_by_id(self, inventory_id, inventory):
        self._inventory_repository.update_by_id(inventory_id, inventory)
