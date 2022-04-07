import unittest
from unittest import mock

from src.api.controllers.chef_controller import ChefController
from src.tests.utils.fixtures.chef_fixture import build_chef, build_chefs


class ChefRepositoryControllerTestCase(unittest.TestCase):
    def setUp(self):
        self.chef_repository = mock.Mock()
        self.chef_controller = ChefController(self.chef_repository)

    def test_add_chef_successfully(self):
        chef = build_chef()

        self.chef_controller.add(chef)

        self.chef_repository.add.assert_called_with(chef)

    def test_get_chef_successfully(self):
        chef = build_chef()

        self.chef_repository.get_by_id.return_value = chef

        expected_chef = self.chef_controller.get_by_id(chef.id)

        self.chef_repository.get_by_id.assert_called_with(chef.id)
        self.assertEqual(expected_chef.id, chef.id)

    def test_get_all_chefs_successfully(self):
        chefs = build_chefs(count=3)

        self.chef_repository.get_all.return_value = chefs

        expected_chefs = self.chef_controller.get_all()

        self.chef_repository.get_all.assert_called()
        self.assertEqual(expected_chefs, chefs)
        self.assertEqual(len(expected_chefs), 3)

    def test_delete_an_chef_successfully(self):
        self.chef_controller.delete_by_id(2)

        self.chef_repository.delete_by_id.assert_called_with(2)

    def test_update_an_chef_successfully(self):
        chef = build_chef()

        self.chef_controller.update_by_id(1, chef)

        self.chef_repository.update_by_id.assert_called_with(1, chef)
