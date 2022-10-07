import unittest
from unittest import mock

from src.api.controllers.inventory_controller import InventoryController
from src.constants.audit import Status
from src.lib.repositories.impl_v2.inventory_repository_impl import (
    InventoryRepositoryImpl,
)

from src.tests.utils.fixtures.mapping_orm_fixtures import (
    build_inventory,
    build_inventories,
)
from src.tests.lib.repositories.sqlalchemy_base_repository_impl_test import (
    SqlAlchemyBaseRepositoryTestCase,
)


class InventoryIngredientRepositoryControllerIntegrationTestCase(
    SqlAlchemyBaseRepositoryTestCase
):
    def after_base_setup(self):

        self.inventory_repository = mock.Mock(
            wraps=InventoryRepositoryImpl(self.mocked_sqlalchemy_session)
        )
        self.inventory_controller = InventoryController(self.inventory_repository)

    def test_add_inventory_to_repository_using_controller(self):
        inventory = build_inventory()

        self.inventory_controller.add(inventory)
        self.inventory_repository.add.assert_called_with(inventory)

    def test_get_inventory_from_repository_using_controller(self):
        inventories = build_inventories(count=3)

        self.inventory_controller.add(inventories[0])
        self.inventory_controller.add(inventories[1])
        self.inventory_controller.add(inventories[2])
        self.inventory_repository.get_by_id.return_value = inventories[2]
        found_inventory2 = self.inventory_controller.get_by_id(2)

        self.inventory_repository.get_by_id.assert_called_with(2)
        self.assertEqual(found_inventory2.id, 1)

    def test_get_all_inventories_from_repository_using_controller(self):

        inventories_to_insert = build_inventories(count=4)

        self.inventory_controller.add(inventories_to_insert[0])
        self.inventory_controller.add(inventories_to_insert[1])
        self.inventory_controller.add(inventories_to_insert[2])
        self.inventory_controller.add(inventories_to_insert[3])
        self.inventory_repository.get_all.return_value = inventories_to_insert
        inventories = self.inventory_controller.get_all()

        self.inventory_repository.get_all.assert_called_with()

        self.assertEqual(
            inventories,
            [
                inventories_to_insert[0],
                inventories_to_insert[1],
                inventories_to_insert[2],
                inventories_to_insert[3],
            ],
        )

    def test_get_all_inventories_empty_from_repository_through_controller(
        self,
    ):
        self.inventory_repository.get_all.return_value = []
        inventories = self.inventory_controller.get_all()
        self.inventory_repository.get_all.assert_called_with()
        self.assertEqual(inventories, [])

    def test_delete_an_inventory_from_repository_using_controller(self):
        inventories_to_insert = build_inventories(count=4)
        inventory_to_delete = build_inventory(entity_status=Status.DELETED)
        self.inventory_controller.add(inventories_to_insert[0])
        self.inventory_controller.add(inventories_to_insert[1])
        self.inventory_controller.add(inventories_to_insert[2])
        self.inventory_controller.add(inventories_to_insert[3])

        self.inventory_controller.delete_by_id(3, inventory_to_delete)
        self.inventory_repository.get_all.return_value = [
            inventories_to_insert[0],
            inventories_to_insert[1],
            inventories_to_insert[3],
        ]
        inventories = self.inventory_controller.get_all()

        self.inventory_repository.delete_by_id.assert_called_once_with(
            3, inventory_to_delete
        )

        self.assertEqual(
            inventories,
            [
                inventories_to_insert[0],
                inventories_to_insert[1],
                inventories_to_insert[3],
            ],
        )

    def test_update_inventory_from_repository_using_controller(self):
        inventories_to_insert = build_inventories(count=2)

        self.inventory_controller.add(inventories_to_insert[0])
        self.inventory_controller.add(inventories_to_insert[1])

        inventory_to_update = build_inventory(update_by="test")
        self.inventory_controller.update_by_id(2, inventory_to_update)
        self.inventory_repository.get_by_id.return_value = inventory_to_update
        updated_inventory = self.inventory_controller.get_by_id(2)
        self.inventory_repository.get_all.return_value = inventories_to_insert
        inventories = self.inventory_controller.get_all()

        self.inventory_repository.update_by_id.assert_called_once_with(
            2, inventory_to_update
        )

        self.assertEqual(len(inventories), 2)
        self.assertEqual(
            updated_inventory.updated_by,
            inventory_to_update.updated_by,
        )
