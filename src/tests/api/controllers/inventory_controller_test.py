import unittest
from unittest import mock

from src.api.controllers import inventory_controller
from src.constants import audit
from src.tests.utils.fixtures import inventory_fixture


class InventoryRepositoryControllerTestCase(unittest.TestCase):
    def setUp(self):
        self.inventory_repository = mock.Mock()
        self.inventory_controller = inventory_controller.InventoryController(
            self.inventory_repository
        )

    def test_add_inventory_successfully(self):
        inventory = inventory_fixture.build_inventory()

        self.inventory_controller.add(inventory)

        self.inventory_repository.add.assert_called_with(inventory)

    def test_get_inventory_successfully(self):
        inventory = inventory_fixture.build_inventory()

        self.inventory_repository.get_by_id.return_value = inventory

        expected_inventory = self.inventory_controller.get_by_id(inventory.id)

        self.inventory_repository.get_by_id.assert_called_with(inventory.id)
        self.assertEqual(expected_inventory.id, inventory.id)

    def test_get_all_inventories_successfully(self):
        inventories = inventory_fixture.build_inventories(count=3)

        self.inventory_repository.get_all.return_value = inventories

        expected_inventories = self.inventory_controller.get_all()

        self.inventory_repository.get_all.assert_called()
        self.assertEqual(expected_inventories, inventories)
        self.assertEqual(len(expected_inventories), 3)

    def test_delete_an_inventory_successfully(self):
        inventory_to_delete = inventory_fixture.build_inventory(
            entity_status=audit.Status.DELETED
        )
        self.inventory_controller.delete_by_id(2, inventory_to_delete)

        self.inventory_repository.delete_by_id.assert_called_with(
            2, inventory_to_delete
        )

    def test_update_an_inventory_successfully(self):
        inventory = inventory_fixture.build_inventory()

        self.inventory_controller.update_by_id(1, inventory)

        self.inventory_repository.update_by_id.assert_called_with(1, inventory)
