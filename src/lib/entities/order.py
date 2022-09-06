# class to process the clients orders
from src.lib.entities import abstract_entity
from src.utils import utils


class Order(abstract_entity.AbstractEntity):
    def __init__(self):

        self.id = None  # integer
        self.status = None  # enum
        self.assigned_chef_id = None  # integer

    def __eq__(self, other):
        return utils.equals(self, other)
