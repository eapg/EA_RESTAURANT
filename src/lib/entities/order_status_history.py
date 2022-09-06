# entity to manage order status history
from src.lib.entities import abstract_entity
from src.utils import utils


class OrderStatusHistory(abstract_entity.AbstractEntity):
    def __init__(self):
        self.id = None  # integer
        self.order_id = None  # integer
        self.from_time = None  # time
        self.to_time = None  # time
        self.from_status = None  # Enum
        self.to_status = None  # Enum

    def __eq__(self, other):
        return utils.equals(self, other)
