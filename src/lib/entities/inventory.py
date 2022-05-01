# class to store the ingredient inventory
from src.utils.utils import equals


class Inventory:
    def __init__(self):

        self.id = None  # integer
        self.inventory_ingredients = {}  # dict

    def __eq__(self, other):
        return equals(self, other)
