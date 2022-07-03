# class for the products of the restaurant ;like pizzas, pasta,lasagna
from src.utils.utils import equals
from src.lib.entities.abstract_entity import AbstractEntity


class Product(AbstractEntity):
    def __init__(self):
        self.id = None  # integer
        self.name = None  # string
        self.description = None  # string

    def __eq__(self, other):
        return equals(self, other)
