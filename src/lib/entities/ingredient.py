# class for the ingredients of the product ; like pizza bread, cheese, sauce
from src.lib.entities import abstract_entity
from src.utils import utils


class Ingredient(abstract_entity.AbstractEntity):
    def __init__(self):

        self.id = None  # integer
        self.name = None  # string
        self.description = None  # string

    def __eq__(self, other):
        return utils.equals(self, other)
