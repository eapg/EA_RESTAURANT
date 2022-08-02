from src.utils.utils import equals
from src.lib.entities.abstract_entity import AbstractEntity


class User(AbstractEntity):

    def __init__(self):

        self.name = None
        self.last_name = None
        self.user_name = None
        self.password = None
        self.role = None
        self.type = None

    def __eq__(self, other):
        return equals(self, other)
