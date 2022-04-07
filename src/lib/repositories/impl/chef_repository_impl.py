# This file has the chef repository

from src.lib.repositories.chef_repository import ChefRepository


class ChefRepositoryImpl(ChefRepository):
    def __init__(self):
        self._chefs = {}
        self._current_id = 1

    def add(self, chef):
        chef.id = self._current_id
        self._chefs[chef.id] = chef
        self._current_id += 1

    def get_by_id(self, chef_id):
        return self._chefs[chef_id]

    def get_all(self):
        return list(self._chefs.values())

    def delete_by_id(self, chef_id):
        self._chefs.pop(chef_id)

    def update_by_id(self, chef_id, chef):
        current_chef = self.get_by_id(chef_id)
        current_chef.name = chef.name or current_chef.name
        current_chef.chef_skills = chef.chef_skills or current_chef.chef_skills
