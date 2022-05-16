# class to create the chefs
from src.utils.utils import equals


class Chef:
    def __init__(self):

        self.id = None  # integer
        self.name = None  # string
        self.chef_skills = None  # string
        self.entity_status = None  # enum
        self.create_date = None  # date
        self.update_date = None  # date
        self.create_by = None  # obj
        self.update_by = None  # obj

    def __eq__(self, other):
        return equals(self, other)
