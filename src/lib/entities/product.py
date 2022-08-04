# class for the products of the restaurant ;like pizzas, pasta,lasagna
from src.lib.entities.abstract_entity import AbstractEntity
from src.utils.utils import equals


class Product(AbstractEntity):
    def __init__(self):
        self.id = None  # integer
        self.name = None  # string
        self.description = None  # string

    def __eq__(self, other):
        return equals(self, other)
