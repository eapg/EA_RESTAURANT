# Interface for the repositories through Abstract method
from abc import ABCMeta

from src.lib.repositories.generic_repository import GenericRepository


class IngredientRepository(GenericRepository, metaclass=ABCMeta):
    pass
