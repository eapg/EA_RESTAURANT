# Interface for the repositories through Abstract method

from abc import ABC, abstractmethod
from injector import Module


class GenericRepository(ABC, Module):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get_by_id(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def delete_by_id(self, obj_id, obj):
        pass

    @abstractmethod
    def update_by_id(self, obj_id, obj):
        pass
