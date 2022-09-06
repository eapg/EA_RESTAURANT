from src.lib.entities import abstract_entity
from src.utils import utils


class Client(abstract_entity.AbstractEntity):
    def __init__(self):
        self.id = None
        self.user_id = None

    def __eq__(self, other):
        return utils.equals(self, other)
