# This file has the chef repository

from src.main.repositories.generic_repository import GeneralRepository


class ChefRepository(GeneralRepository):

    def __init__(self):
        self.__chefs = {}
        self.__current_id = 0

    def add(self, chef):
        chef.id = self.__current_id
        self.__chefs[chef.id] = chef
        self.__current_id += 1

    def get_by_id(self, chef_id):
        return self.__chefs[chef_id]

    def get_all(self):
        return self.__chefs.values()

    def delete_by_id(self, chef_id):
        self.__chefs.pop(chef_id)

    def update_by_id(self, chef_id, chef):
        current_chef = self.get_by_id(chef_id)
        current_chef.name = chef.name
        current_chef.chef_skills = chef.chef_skills

