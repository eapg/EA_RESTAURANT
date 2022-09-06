# This entity will be used to store the Ingredient and its quantity
from src.lib.entities import abstract_entity
from src.utils import utils


class InventoryIngredient(abstract_entity.AbstractEntity):
    def __init__(self):

        self.id = None  # integer
        self.ingredient_id = None  # integer
        self.inventory_id = None  # integer
        self.quantity = None  # integer

    def __eq__(self, other):
        return utils.equals(self, other)
