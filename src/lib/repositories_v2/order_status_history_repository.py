# Interface for the repositories through Abstract method
from abc import ABCMeta, abstractmethod

from src.lib.repositories.generic_repository import GenericRepository


class OrderStatusHistoryRepository(GenericRepository, metaclass=ABCMeta):
    @abstractmethod
    def get_by_order_id(self, order_id):
        pass

    @abstractmethod
    def set_next_status_history_by_order_id(self, order_id, new_status):
        pass
