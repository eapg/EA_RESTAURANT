# class to store the ingredient inventory
from src.lib.entities.abstract_entity import AbstractEntity
from src.utils.utils import equals


class Inventory(AbstractEntity):
    def __init__(self):

        self.id = None  # integer

    def __eq__(self, other):
        return equals(self, other)
