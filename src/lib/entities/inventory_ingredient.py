# This entity will be used to store the Ingredient and its quantity
from src.utils.utils import equals


class InventoryIngredient:
    def __init__(self):

        self.id = None  # integer
        self.ingredient = None  # object
        self.inventory = None # object
        self.ingredient_quantity = None  # integer
        self.entity_status = None  # enum
        self.create_date = None  # date
        self.update_date = None  # date
        self.create_by = None  # obj
        self.update_by = None  # obj

    def __eq__(self, other):
        return equals(self, other)
