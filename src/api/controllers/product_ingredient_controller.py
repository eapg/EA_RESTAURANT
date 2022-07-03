class ProductIngredientController:
    def __init__(self, product_ingredient_repository):
        self._product_ingredient_repository = (
            product_ingredient_repository  # ProductIngredientRepository
        )

    def add(self, product_ingredient):
        self._product_ingredient_repository.add(product_ingredient)

    def get_by_id(self, product_ingredient_id):
        return self._product_ingredient_repository.get_by_id(product_ingredient_id)

    def get_all(self):
        return self._product_ingredient_repository.get_all()

    def delete_by_id(self, product_ingredient_id, product_ingredient):
        self._product_ingredient_repository.delete_by_id(
            product_ingredient_id, product_ingredient
        )

    def update_by_id(self, product_ingredient_id, product_ingredient):
        self._product_ingredient_repository.update_by_id(
            product_ingredient_id, product_ingredient
        )

    def get_by_product_id(self, product_id):
        return self._product_ingredient_repository.get_by_product_id(product_id)
