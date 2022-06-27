# class for the ingredients of the product ; like pizza bread, cheese, sauce
from src.utils.utils import equals
from src.lib.entities.abstract_entity import AbstractEntity


class Ingredient(AbstractEntity):
    def __init__(self):

        self.id = None  # integer
        self.name = None  # string
        self.description = None  # string

    def __eq__(self, other):
        return equals(self, other)
