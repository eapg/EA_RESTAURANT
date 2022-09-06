from src.lib.entities import abstract_entity
from src.utils import utils


class OrderDetail(abstract_entity.AbstractEntity):
    def __init__(self):
        self.id = None  # integer
        self.order_id = None  # integer
        self.product_id = None  # integer
        self.quantity = None  # integer

    def __eq__(self, other):
        return utils.equals(self, other)
