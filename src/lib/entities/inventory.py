# class to store the ingredient inventory
from src.utils.utils import equals


class Inventory:
    def __init__(self):

        self.id = None  # integer
        self.entity_status = None  # enum
        self.create_date = None  # date
        self.update_date = None  # date
        self.create_by = None  # obj
        self.update_by = None  # obj

    def __eq__(self, other):
        return equals(self, other)
