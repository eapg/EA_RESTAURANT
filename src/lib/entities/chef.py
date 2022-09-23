# class to create the chefs
from src.lib.entities.abstract_entity import AbstractEntity
from src.utils.utils import equals


class Chef(AbstractEntity):
    def __init__(self):

        self.id = None  # integer
        self.name = None  # string
        self.skill = None  # integer

    def __eq__(self, other):
        return equals(self, other)
