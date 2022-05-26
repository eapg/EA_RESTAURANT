class ChefController:
    def __init__(self, chef_repository):
        self._chef_repository = chef_repository  # chefRepository

    def add(self, chef):
        self._chef_repository.add(chef)

    def get_by_id(self, chef_id):
        return self._chef_repository.get_by_id(chef_id)

    def get_all(self):
        return self._chef_repository.get_all()

    def delete_by_id(self, chef_id):
        self._chef_repository.delete_by_id(chef_id)

    def update_by_id(self, chef_id, chef):
        self._chef_repository.update_by_id(chef_id, chef)

    def get_available_chefs(self):
        return self._chef_repository.get_available_chefs()
