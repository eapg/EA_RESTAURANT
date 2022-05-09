# entity to relate the product with the ingredient and the quantity that the product need.
from src.utils.utils import equals


class ProductIngredient:
    def __init__(self):
        self.id = None  # integer
        self.product = None  # object
        self.ingredient = None  # object
        self.quantity = None  # integer

    def __eq__(self, other):
        return equals(self, other)
