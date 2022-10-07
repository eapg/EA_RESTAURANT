# Interface for the repositories through Abstract method
from abc import ABCMeta, abstractmethod

from src.lib.repositories.generic_repository import GenericRepository


class ChefRepository(GenericRepository, metaclass=ABCMeta):
    @abstractmethod
    def get_available_chefs(self):
        pass
