# class for the products of the restaurant ;like pizzas, pasta,lasagna
from src.utils.utils import equals


class Product:
    def __init__(self):

        self.id = None  # integer
        self.name = None  # string
        self.description = None  # string
        self.ingredients = []  # list

    def __eq__(self, other):
        return equals(self, other)
