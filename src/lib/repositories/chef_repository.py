# Interface for the repositories through Abstract method
from abc import ABCMeta, abstractmethod

from src.lib.repositories import generic_repository


class ChefRepository(generic_repository.GenericRepository, metaclass=ABCMeta):
    @abstractmethod
    def get_available_chefs(self):
        pass
