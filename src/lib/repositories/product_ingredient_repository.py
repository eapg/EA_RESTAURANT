# Interface for the repositories through Abstract method
from abc import ABCMeta, abstractmethod

from src.lib.repositories import generic_repository


class ProductIngredientRepository(generic_repository.GenericRepository, metaclass=ABCMeta):
    @abstractmethod
    def get_by_product_id(self, product_id):
        pass

    @abstractmethod
    def get_product_ingredients_by_product_ids(self, product_ids):
        pass
