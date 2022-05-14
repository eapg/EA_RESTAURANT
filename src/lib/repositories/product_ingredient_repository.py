# Interface for the repositories through Abstract method
from abc import ABCMeta, abstractmethod

from src.lib.repositories.generic_repository import GenericRepository


class ProductIngredientRepository(GenericRepository, metaclass=ABCMeta):

    @abstractmethod
    def get_by_product_id(self, product):
        pass
