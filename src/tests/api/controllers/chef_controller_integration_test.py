import unittest
from unittest import mock

from src.api.controllers.chef_controller import ChefController
from src.lib.repositories.impl.chef_repository_impl import ChefRepositoryImpl
from src.tests.utils.fixtures.chef_fixture import build_chef, build_chefs


class ChefRepositoryControllerIntegrationTestCase(unittest.TestCase):
    def setUp(self):
        self.chef_repository = mock.Mock(wraps=ChefRepositoryImpl())
        self.chef_controller = ChefController(self.chef_repository)

    def test_add_chef_to_repository_using_controller(self):
        chef = build_chef()

        self.assertIsNone(chef.id)

        self.chef_controller.add(chef)
        self.chef_repository.add.assert_called_with(chef)

    def test_get_chef_from_repository_using_controller(self):
        chefs = build_chefs(count=3)

        self.chef_controller.add(chefs[0])
        self.chef_controller.add(chefs[1])
        self.chef_controller.add(chefs[2])

        found_chef3 = self.chef_controller.get_by_id(3)

        self.chef_repository.get_by_id.assert_called_with(3)
        self.assertEqual(found_chef3.id, 3)

    def test_get_throws_key_error_for_non_existing_chef(self):
        chef1 = build_chef()

        self.chef_controller.add(chef1)

        self.assertRaises(KeyError, self.chef_controller.get_by_id, 2)
        self.chef_repository.get_by_id.assert_called_with(2)

    def test_get_all_chefs_from_repository_using_controller(self):

        chefs_to_insert = build_chefs(count=4)

        self.chef_controller.add(chefs_to_insert[0])
        self.chef_controller.add(chefs_to_insert[1])
        self.chef_controller.add(chefs_to_insert[2])
        self.chef_controller.add(chefs_to_insert[3])

        chefs = self.chef_controller.get_all()

        self.chef_repository.get_all.assert_called_with()

        self.assertEqual(
            chefs,
            [
                chefs_to_insert[0],
                chefs_to_insert[1],
                chefs_to_insert[2],
                chefs_to_insert[3],
            ],
        )

    def test_get_all_chefs_empty_from_repository_through_controller(self):
        chefs = self.chef_controller.get_all()
        self.chef_repository.get_all.assert_called_with()
        self.assertEqual(chefs, [])

    def test_delete_an_chef_from_repository_using_controller(self):
        chefs_to_insert = build_chefs(count=4)

        self.chef_controller.add(chefs_to_insert[0])
        self.chef_controller.add(chefs_to_insert[1])
        self.chef_controller.add(chefs_to_insert[2])
        self.chef_controller.add(chefs_to_insert[3])

        self.chef_controller.delete_by_id(3)
        chefs = self.chef_controller.get_all()

        self.chef_repository.delete_by_id.assert_called_once_with(3)

        self.assertEqual(
            chefs,
            [
                chefs_to_insert[0],
                chefs_to_insert[1],
                chefs_to_insert[3],
            ],
        )

    def test_delete_throws_key_error_when_there_are_no_chefs(self):
        self.assertRaises(KeyError, self.chef_controller.delete_by_id, 3)
        self.chef_repository.delete_by_id.assert_called_with(3)

    def test_update_chef_from_repository_using_controller(self):
        chefs_to_insert = build_chefs(count=2)

        self.chef_controller.add(chefs_to_insert[0])
        self.chef_controller.add(chefs_to_insert[1])

        chef_to_update = build_chef(chef_skills="advance")

        self.chef_controller.update_by_id(2, chef_to_update)
        updated_chef = self.chef_controller.get_by_id(2)
        chefs = self.chef_controller.get_all()

        self.chef_repository.update_by_id.assert_called_once_with(2, chef_to_update)

        self.assertEqual(len(chefs), 2)
        self.assertEqual(updated_chef.chef_skills, chef_to_update.chef_skills)
