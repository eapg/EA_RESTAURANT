# entity to relate the product with the ingredient and the quantity that the product need.
from src.utils.utils import equals


class ProductIngredient:
    def __init__(self):
        self.id = None  # integer
        self.product_id = None  # integer
        self.ingredient_id = None  # integer
        self.quantity = None  # integer
        self.ingredient_type = None  # string
        self.entity_status = None  # enum
        self.create_date = None  # date
        self.update_date = None  # date
        self.create_by = None  # obj
        self.update_by = None  # obj

    def __eq__(self, other):
        return equals(self, other)
