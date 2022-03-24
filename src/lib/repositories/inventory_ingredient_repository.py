# Interface for the repositories through Abstract method
from abc import ABCMeta

from src.main.repositories.generic_repository import GeneralRepository


class InventoryIngredientRepository(GenericRepository, metaclass=ABCMeta):
    pass
