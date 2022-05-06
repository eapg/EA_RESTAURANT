# Interface for the repositories through Abstract method
from abc import ABCMeta

from src.lib.repositories.generic_repository import GenericRepository


class OrderRepository(GenericRepository, metaclass=ABCMeta):
    @staticmethod
    def get_orders_to_process():
        pass
