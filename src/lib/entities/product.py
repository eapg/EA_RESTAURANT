# class for the products of the restaurant ;like pizzas, pasta,lasagna
from src.lib.entities.abstract_entity import AbstractEntity, AbstractCommonAttributesEntity
from src.utils.utils import equals


class Product(AbstractEntity, AbstractCommonAttributesEntity ):

    def __init__(self):
        pass

    def __eq__(self, other):
        return equals(self, other)
