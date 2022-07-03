# This entity will be used to store the Ingredient and its quantity
from src.utils.utils import equals
from src.lib.entities.abstract_entity import AbstractEntity


class InventoryIngredient(AbstractEntity):
    def __init__(self):

        self.id = None  # integer
        self.ingredient_id = None  # integer
        self.inventory_id = None  # integer
        self.ingredient_quantity = None  # integer

    def __eq__(self, other):
        return equals(self, other)
