import unittest
from unittest import mock

from src.api.controllers import chef_controller
from src.constants import audit
from src.constants.order_status import OrderStatus
from src.lib.repositories.impl import chef_repository_impl
from src.lib.repositories.impl import order_repository_impl
from src.tests.utils.fixtures import chef_fixture
from src.tests.utils.fixtures import order_fixture


class ChefRepositoryControllerIntegrationTestCase(unittest.TestCase):
    def setUp(self):

        self.order_repository = mock.Mock(
            wraps=order_repository_impl.OrderRepositoryImpl()
        )
        self.chef_repository = mock.Mock(
            wraps=chef_repository_impl.ChefRepositoryImpl(self.order_repository)
        )
        self.chef_controller = chef_controller.ChefController(self.chef_repository)

    def test_add_chef_to_repository_using_controller(self):
        chef = chef_fixture.build_chef()

        self.chef_controller.add(chef)
        self.chef_repository.add.assert_called_with(chef)
        self.assertEqual(chef.id, 1)

    def test_get_chef_from_repository_using_controller(self):
        chefs = chef_fixture.build_chefs(count=3)

        self.chef_controller.add(chefs[0])
        self.chef_controller.add(chefs[1])
        self.chef_controller.add(chefs[2])

        found_chef3 = self.chef_controller.get_by_id(3)

        self.chef_repository.get_by_id.assert_called_with(3)
        self.assertEqual(found_chef3.id, 3)

    def test_get_throws_key_error_for_non_existing_chef(self):
        chef1 = chef_fixture.build_chef()

        self.chef_controller.add(chef1)

        self.assertRaises(KeyError, self.chef_controller.get_by_id, 2)
        self.chef_repository.get_by_id.assert_called_with(2)

    def test_get_all_chefs_from_repository_using_controller(self):

        chefs_to_insert = chef_fixture.build_chefs(count=4)

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
        chefs_to_insert = chef_fixture.build_chefs(count=4)
        chef_to_delete = chef_fixture.build_chef(entity_status=audit.Status.DELETED)
        self.chef_controller.add(chefs_to_insert[0])
        self.chef_controller.add(chefs_to_insert[1])
        self.chef_controller.add(chefs_to_insert[2])
        self.chef_controller.add(chefs_to_insert[3])

        self.chef_controller.delete_by_id(3, chef_to_delete)
        chefs = self.chef_controller.get_all()

        self.chef_repository.delete_by_id.assert_called_once_with(3, chef_to_delete)

        self.assertEqual(
            chefs,
            [
                chefs_to_insert[0],
                chefs_to_insert[1],
                chefs_to_insert[3],
            ],
        )

    def test_delete_throws_key_error_when_there_are_no_chefs(self):
        chef_to_delete = chef_fixture.build_chef(entity_status=audit.Status.DELETED)
        self.assertRaises(
            KeyError, self.chef_controller.delete_by_id, 3, chef_to_delete
        )
        self.chef_repository.delete_by_id.assert_called_with(3, chef_to_delete)

    def test_update_chef_from_repository_using_controller(self):
        chefs_to_insert = chef_fixture.build_chefs(count=2)

        self.chef_controller.add(chefs_to_insert[0])
        self.chef_controller.add(chefs_to_insert[1])

        chef_to_update = chef_fixture.build_chef(chef_skills="advance")

        self.chef_controller.update_by_id(2, chef_to_update)
        updated_chef = self.chef_controller.get_by_id(2)
        chefs = self.chef_controller.get_all()

        self.chef_repository.update_by_id.assert_called_once_with(2, chef_to_update)

        self.assertEqual(len(chefs), 2)
        self.assertEqual(updated_chef.chef_skills, chef_to_update.chef_skills)

    def test_get_available_chefs_from_repository_using_controller(self):

        chef_principal = chef_fixture.build_chef(
            chef_id=1, name="Elido p", chef_skills=5
        )
        chef_intermediate = chef_fixture.build_chef(
            chef_id=2, name="Andres p", chef_skills=3
        )
        chef_basic = chef_fixture.build_chef(chef_id=3, name="Juan p", chef_skills=1)

        order_1 = order_fixture.build_order(
            assigned_chef_id=chef_intermediate.id, status=OrderStatus.IN_PROCESS
        )
        order_2 = order_fixture.build_order(assigned_chef_id=None)
        order_3 = order_fixture.build_order(assigned_chef_id=None)

        self.order_repository.add(order_1)
        self.order_repository.add(order_2)
        self.order_repository.add(order_3)

        self.chef_controller.add(chef_principal)
        self.chef_controller.add(chef_intermediate)
        self.chef_controller.add(chef_basic)

        available_chefs = self.chef_controller.get_available_chefs()
        self.chef_repository.get_available_chefs.assert_called()
        self.order_repository.get_chefs_with_assigned_orders.assert_called_with(
            [chef_principal.id, chef_intermediate.id, chef_basic.id]
        )
        self.assertEqual(available_chefs, [chef_principal.id, chef_basic.id])
