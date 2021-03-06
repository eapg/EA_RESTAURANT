class InventoryIngredientController:
    def __init__(self, inventory_ingredient_repository):
        self._inventory_ingredient_repository = (
            inventory_ingredient_repository  # inventory_ingredientRepository
        )

    def add(self, inventory_ingredient):
        self._inventory_ingredient_repository.add(inventory_ingredient)

    def get_by_id(self, inventory_ingredient_id):
        return self._inventory_ingredient_repository.get_by_id(inventory_ingredient_id)

    def get_all(self):
        return self._inventory_ingredient_repository.get_all()

    def delete_by_id(self, inventory_ingredient_id, inventory_ingredient):
        self._inventory_ingredient_repository.delete_by_id(
            inventory_ingredient_id, inventory_ingredient
        )

    def update_by_id(self, inventory_ingredient_id, inventory_ingredient):
        self._inventory_ingredient_repository.update_by_id(
            inventory_ingredient_id, inventory_ingredient
        )

    def get_by_ingredient_id(self, ingredient_id):
        return self._inventory_ingredient_repository.get_by_ingredient_id(ingredient_id)

    def validate_ingredient_availability(
        self, inventory_id, ingredient_id, quantity_to_use
    ):
        return self._inventory_ingredient_repository.validate_ingredient_availability(
            inventory_id, ingredient_id, quantity_to_use
        )
