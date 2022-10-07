from src.lib.entities.abstract_entity import AbstractEntity
from src.utils.utils import equals


class Client(AbstractEntity):
    def __init__(self):
        self.id = None
        self.user_id = None

    def __eq__(self, other):
        return equals(self, other)
