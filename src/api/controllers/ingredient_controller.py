class IngredientController:
    def __init__(self, ingredient_repository):
        self._ingredient_repository = ingredient_repository  # IngredientRepository

    def add(self, ingredient):
        self._ingredient_repository.add(ingredient)

    def get_by_id(self, ingredient_id):
        return self._ingredient_repository.get_by_id(ingredient_id)

    def get_all(self):
        return self._ingredient_repository.get_all()

    def delete_by_id(self, ingredient_id, ingredient):
        self._ingredient_repository.delete_by_id(ingredient_id, ingredient)

    def update_by_id(self, ingredient_id, ingredient):
        self._ingredient_repository.update_by_id(ingredient_id, ingredient)
