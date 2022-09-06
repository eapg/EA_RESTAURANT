# class for the products of the restaurant ;like pizzas, pasta,lasagna
from src.lib.entities import abstract_entity
from src.utils import utils


class Product(abstract_entity.AbstractEntity):
    def __init__(self):
        self.id = None  # integer
        self.name = None  # string
        self.description = None  # string

    def __eq__(self, other):
        return utils.equals(self, other)
