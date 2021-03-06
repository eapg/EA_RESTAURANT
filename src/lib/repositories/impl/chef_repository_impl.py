# This file has the chef repository
from datetime import datetime

from src.constants.audit import Status
from src.lib.repositories.chef_repository import ChefRepository


class ChefRepositoryImpl(ChefRepository):
    def __init__(self, order_repository=None):
        self._chefs = {}
        self._current_id = 1
        self.order_repository = order_repository

    def add(self, chef):
        chef.id = self._current_id
        chef.create_date = datetime.now()
        chef.update_by = chef.create_by
        chef.update_date = chef.create_date
        self._chefs[chef.id] = chef
        self._current_id += 1

    def get_by_id(self, chef_id):
        chef_to_return = self._chefs[chef_id]
        chef_filtered = list(
            filter(
                lambda chef: chef.entity_status == Status.ACTIVE,
                [chef_to_return],
            )
        )
        return chef_filtered[0]

    def get_all(self):
        chefs = list(self._chefs.values())
        chefs_filtered = filter(lambda chef: chef.entity_status == Status.ACTIVE, chefs)
        return list(chefs_filtered)

    def delete_by_id(self, chef_id, chef):
        chef_to_be_delete = self.get_by_id(chef_id)
        chef_to_be_delete.entity_status = Status.DELETED
        chef_to_be_delete.update_date = datetime.now()
        chef_to_be_delete.update_by = chef.update_by
        self._update_by_id(chef_id, chef_to_be_delete, use_merge_with_existing=False)

    def update_by_id(self, chef_id, chef):
        self._update_by_id(chef_id, chef)

    def _update_by_id(self, chef_id, chef, use_merge_with_existing=True):
        current_chef = self.get_by_id(chef_id) if use_merge_with_existing else chef
        current_chef.name = chef.name or current_chef.name
        current_chef.chef_skills = chef.chef_skills or current_chef.chef_skills
        current_chef.update_date = datetime.now()
        current_chef.update_by = chef.update_by or current_chef.update_by
        current_chef.entity_status = chef.entity_status or current_chef.entity_status

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
