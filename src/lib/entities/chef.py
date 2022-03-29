# class to create the chefs
from src.utils.utils import equals


class Chef:
    def __init__(self):

        self.id = None  # integer
        self.name = None  # string
        self.chef_skills = None  # string

    def __eq__(self, other):
        return equals(self, other)
