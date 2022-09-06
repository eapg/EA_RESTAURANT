# class to store the ingredient inventory
from src.lib.entities import abstract_entity
from src.utils import utils


class Inventory(abstract_entity.AbstractEntity):
    def __init__(self):

        self.id = None  # integer

    def __eq__(self, other):
        return utils.equals(self, other)
