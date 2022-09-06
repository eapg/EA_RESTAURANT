# entity to relate the product with the ingredient and the quantity that the product need.
from src.lib.entities import abstract_entity
from src.utils import utils


class ProductIngredient(abstract_entity.AbstractEntity):
    def __init__(self):
        self.id = None  # integer
        self.product_id = None  # integer
        self.ingredient_id = None  # integer
        self.quantity = None  # integer
        self.ingredient_type = None  # string

    def __eq__(self, other):
        return utils.equals(self, other)
