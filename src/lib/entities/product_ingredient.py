# entity to relate the product with the ingredient and the quantity that the product need.
from src.utils.utils import equals
from src.lib.entities.abstract_entity import AbstractEntity


class ProductIngredient(AbstractEntity):
    def __init__(self):
        self.id = None  # integer
        self.product_id = None  # integer
        self.ingredient_id = None  # integer
        self.quantity = None  # integer
        self.ingredient_type = None  # string

    def __eq__(self, other):
        return equals(self, other)
