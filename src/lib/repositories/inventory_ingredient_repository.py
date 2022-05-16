# Interface for the repositories through Abstract method
from abc import ABCMeta, abstractmethod

from src.lib.repositories.generic_repository import GenericRepository


class InventoryIngredientRepository(GenericRepository, metaclass=ABCMeta):
    @abstractmethod
    def get_by_ingredient_id(self, ingredient):
        pass
