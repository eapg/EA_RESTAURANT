import unittest

from src.lib.repositories.impl.chef_repository_impl import ChefRepositoryImpl
from src.tests.utils.fixtures.chef_fixture import build_chef, build_chefs


class ChefRepositoryImplTestCase(unittest.TestCase):
    def test_add_chef_successfully(self):
        chef = build_chef()
        chef_repository = ChefRepositoryImpl()

        self.assertIsNone(chef.id)

        chef_repository.add(chef)

        self.assertEqual(chef.id, 1)

    def test_get_chef_successfully(self):
        chefs = build_chefs(count=3)

        chef_repository = ChefRepositoryImpl()

        chef_repository.add(chefs[0])
        chef_repository.add(chefs[1])
        chef_repository.add(chefs[2])

        found_chef3 = chef_repository.get_by_id(3)

        self.assertEqual(found_chef3.id, 3)

    def test_get_throws_key_error_for_non_existing_chef(self):
        chef1 = build_chef()

        chef_repository = ChefRepositoryImpl()

        chef_repository.add(chef1)

        self.assertRaises(KeyError, chef_repository.get_by_id, 2)

    def test_get_all_chefs_successfully(self):
        chefs_to_insert = build_chefs(count=5)

        chef_repository = ChefRepositoryImpl()

        chef_repository.add(chefs_to_insert[0])
        chef_repository.add(chefs_to_insert[1])
        chef_repository.add(chefs_to_insert[2])
        chef_repository.add(chefs_to_insert[3])
        chef_repository.add(chefs_to_insert[4])

        chefs = chef_repository.get_all()

        self.assertEqual(
            chefs,
            [
                chefs_to_insert[0],
                chefs_to_insert[1],
                chefs_to_insert[2],
                chefs_to_insert[3],
                chefs_to_insert[4],
            ],
        )

    def test_get_all_chefs_empty_successfully(self):
        chef_repository = ChefRepositoryImpl()

        chefs = chef_repository.get_all()

        self.assertEqual(chefs, [])

    def test_delete_an_chef_successfully(self):
        chefs_to_insert = build_chefs(count=3)

        chef_repository = ChefRepositoryImpl()

        chef_repository.add(chefs_to_insert[0])
        chef_repository.add(chefs_to_insert[1])
        chef_repository.add(chefs_to_insert[2])

        chef_repository.delete_by_id(2)

        chefs = chef_repository.get_all()

        self.assertEqual(chefs, [chefs_to_insert[0], chefs_to_insert[2]])

    def test_delete_throws_key_error_when_there_are_no_chefs(self):
        chef_repository = ChefRepositoryImpl()

        self.assertRaises(KeyError, chef_repository.delete_by_id, 2)

    def test_update_chef_successfully(self):
        chefs_to_insert = build_chefs(count=2)

        chef_repository = ChefRepositoryImpl()

        chef_repository.add(chefs_to_insert[0])
        chef_repository.add(chefs_to_insert[1])

        chef_to_update = build_chef(chef_skills="advance")

        chef_repository.update_by_id(2, chef_to_update)
        updated_chef = chef_repository.get_by_id(2)
        chefs = chef_repository.get_all()

        self.assertEqual(len(chefs), 2)
        self.assertEqual(updated_chef.chef_skills, chef_to_update.chef_skills)