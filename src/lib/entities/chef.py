# class to create the chefs
from src.utils.utils import equals
from src.lib.entities.abstract_entity import AbstractEntity


class Chef(AbstractEntity):
    def __init__(self):

        self.id = None  # integer
        self.name = None  # string
        self.chef_skills = None  # integer

    def __eq__(self, other):
        return equals(self, other)
