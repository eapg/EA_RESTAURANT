# entity to manage order status history
from src.utils.utils import equals
from src.lib.entities.abstract_entity import AbstractEntity


class OrderStatusHistory(AbstractEntity):
    def __init__(self):
        self.id = None  # integer
        self.order_id = None  # integer
        self.from_time = None  # time
        self.to_time = None  # time
        self.from_status = None  # Enum
        self.to_status = None  # Enum

    def __eq__(self, other):
        return equals(self, other)
