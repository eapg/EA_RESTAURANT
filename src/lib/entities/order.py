# class to process the clients orders
from src.utils.utils import equals


class Order:
    def __init__(self):

        self.id = None  # integer
        self.order_details = None  # list
        self.status = None  # enum
        self.assigned_chef = None  # object
        self.entity_status = None  # enum
        self.create_date = None  # date
        self.update_date = None  # date
        self.create_by = None  # obj
        self.update_by = None  # obj

    def __eq__(self, other):
        return equals(self, other)
