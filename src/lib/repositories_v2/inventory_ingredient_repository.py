# Interface for the repositories through Abstract method
from abc import ABCMeta, abstractmethod

from src.lib.repositories.generic_repository import GenericRepository


class InventoryIngredientRepository(GenericRepository, metaclass=ABCMeta):
    @abstractmethod
    def get_by_ingredient_id(self, ingredient_id):
        pass

    @abstractmethod
    def get_final_product_qty_by_product_ids(self, product_ids):
        pass
