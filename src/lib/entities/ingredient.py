# class for the ingredients of the product ; like pizza bread, cheese, sauce
from src.utils.utils import equals


class Ingredient:
    def __init__(self):

        self.id = None  # integer
        self.name = None  # string
        self.description = None  # string
        self.ingredient_type = None  # string
        self.entity_status = None  # enum
        self.create_date = None  # date
        self.update_date = None  # date
        self.create_by = None  # obj
        self.update_by = None  # obj

    def __eq__(self, other):
        return equals(self, other)
