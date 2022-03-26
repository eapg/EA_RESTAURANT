# Interface for the repositories through Abstract method
from abc import ABCMeta
from lib.repositories.generic_repository import GenericRepository


class ProductRepository(GenericRepository, metaclass=ABCMeta):
    pass
