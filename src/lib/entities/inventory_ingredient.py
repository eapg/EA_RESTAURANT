# This entity will be used to store the Ingredient and its quantity
from src.lib.entities.abstract_entity import AbstractEntity
from src.utils.utils import equals


class InventoryIngredient(AbstractEntity):
    def __init__(self):

        self.id = None  # integer
        self.ingredient_id = None  # integer
        self.inventory_id = None  # integer
        self.quantity = None  # integer

    def __eq__(self, other):
        return equals(self, other)
