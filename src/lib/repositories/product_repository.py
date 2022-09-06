# Interface for the repositories through Abstract method
from abc import ABCMeta

from src.lib.repositories import generic_repository


class ProductRepository(generic_repository.GenericRepository, metaclass=ABCMeta):
    pass
