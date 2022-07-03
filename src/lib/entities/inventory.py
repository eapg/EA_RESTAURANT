# class to store the ingredient inventory
from src.utils.utils import equals
from src.lib.entities.abstract_entity import AbstractEntity


class Inventory(AbstractEntity):
    def __init__(self):

        self.id = None  # integer

    def __eq__(self, other):
        return equals(self, other)
