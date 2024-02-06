# class for the ingredients of the product ; like pizza bread, cheese, sauce
from src.lib.entities.abstract_entity import AbstractEntity, AbstractCommonAttributesEntity
from src.utils.utils import equals


class Ingredient(AbstractEntity, AbstractCommonAttributesEntity):

    def __init__(self):

        pass

    def __eq__(self, other):
        return equals(self, other)
