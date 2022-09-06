# Interface for the repositories through Abstract method
from abc import ABCMeta, abstractmethod

from src.lib.repositories import generic_repository


class InventoryIngredientRepository(
    generic_repository.GenericRepository, metaclass=ABCMeta
):
    @abstractmethod
    def get_by_ingredient_id(self, ingredient_id):
        pass

    @abstractmethod
    def validate_ingredient_availability(
        self, inventory_id, ingredient_id, quantity_to_use
    ):
        pass

    @abstractmethod
    def get_final_product_qty_by_product_ids(self, product_ids):
        pass
