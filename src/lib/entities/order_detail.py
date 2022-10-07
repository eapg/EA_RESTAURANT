from src.lib.entities.abstract_entity import AbstractEntity
from src.utils.utils import equals


class OrderDetail(AbstractEntity):
    def __init__(self):
        self.id = None  # integer
        self.order_id = None  # integer
        self.product_id = None  # integer
        self.quantity = None  # integer

    def __eq__(self, other):
        return equals(self, other)
