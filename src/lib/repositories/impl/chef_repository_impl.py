# This file has the chef repository

from src.lib.repositories.chef_repository import ChefRepository


class ChefRepositoryImpl(ChefRepository):
    def __init__(self, order_repository=None):
        self._chefs = {}
        self._current_id = 1
        self.order_repository = order_repository

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

    def get_available_chefs(self):
        chefs = self.get_all()
        chef_ids = [chef.id for chef in chefs]

        assigned_chef_map = self.order_repository.get_chefs_with_assigned_orders(
            chef_ids
        )
        available_chef_ids = list(
            filter((lambda chef_id: assigned_chef_map[chef_id] == []), chef_ids)
        )

        return available_chef_ids
