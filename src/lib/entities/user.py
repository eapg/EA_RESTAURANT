from src.lib.entities import abstract_entity
from src.utils import utils


class User(abstract_entity.AbstractEntity):
    def __init__(self):

        self.name = None
        self.last_name = None
        self.user_name = None
        self.password = None
        self.role = None
        self.type = None

    def __eq__(self, other):
        return utils.equals(self, other)
