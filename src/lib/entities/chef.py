# class to create the chefs
from src.lib.entities import abstract_entity
from src.utils import utils


class Chef(abstract_entity.AbstractEntity):
    def __init__(self):

        self.id = None  # integer
        self.name = None  # string
        self.chef_skills = None  # integer

    def __eq__(self, other):
        return utils.equals(self, other)
