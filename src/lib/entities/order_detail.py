# class for the order details
from src.utils.utils import equals


class OrderDetail:
    def __init__(self):

        self.id = None  # integer

    def __eq__(self, other):
        return equals(self, other)
