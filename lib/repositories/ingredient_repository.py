# This file has the ingredient repository

from lib.repositories.generic_repository import GenericRepository


class IngredientRepository(GenericRepository):

    def __init__(self):
        self.__ingredients = {}
        self.__current_id = 0

    def add(self, ingredient):
        ingredient.id = self.__current_id
        self.__ingredients[ingredient.id] = ingredient
        self.__current_id += 1

    def get_by_id(self, ingredient_id):
        return self.__ingredients[ingredient_id]

    def get_all(self):
        return self.__ingredients.values()

    def delete_by_id(self, ingredient_id):
        self.__ingredients.pop(ingredient_id)

    def update_by_id(self, ingredient_id, ingredient):
        current_ingredient = self.get_by_id(ingredient_id)
        current_ingredient.name = ingredient.name
        current_ingredient.description = ingredient.description


