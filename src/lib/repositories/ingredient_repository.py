# Interface for the repositories through Abstract method
from abc import ABCMeta

from src.lib.repositories import generic_repository


class IngredientRepository(generic_repository.GenericRepository, metaclass=ABCMeta):
    pass
