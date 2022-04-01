# This entity will be used to store the Ingredient and its quantity
from src.utils.utils import equals


class InventoryIngredient:
    def __init__(self):

        self.id = None  # integer
        self.ingredient = None  # object
        self.ingredient_quantity = None  # integer

    def __eq__(self, other):
        return equals(self, other)