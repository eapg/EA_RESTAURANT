# class to process the clients orders
from src.utils.utils import equals


class Order:
    def __init__(self):

        self.id = None  # integer
        self.order_details = None  # list
        self.status = None  # enum
        self.assigned_chef = None  # object

    def __eq__(self, other):
        return equals(self, other)
