# class to process the clients orders
from src.utils.utils import equals


class Order:
    def __init__(self):

        self.id = None  # integer
        self.status = None  # enum
        self.assigned_chef_id = None  # integer
        self.estimated_time = None  # integer
        self.entity_status = None  # enum
        self.create_date = None  # date
        self.update_date = None  # date
        self.create_by = None  # obj
        self.update_by = None  # obj

    def __eq__(self, other):
        return equals(self, other)
