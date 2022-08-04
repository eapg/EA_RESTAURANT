# class to process the clients orders
from src.lib.entities.abstract_entity import AbstractEntity
from src.utils.utils import equals


class Order(AbstractEntity):
    def __init__(self):

        self.id = None  # integer
        self.status = None  # enum
        self.assigned_chef_id = None  # integer

    def __eq__(self, other):
        return equals(self, other)
