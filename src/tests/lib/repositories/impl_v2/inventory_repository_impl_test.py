from unittest import mock

from src.constants import audit
from src.lib.entities import sqlalchemy_orm_mapping
from src.lib.repositories.impl_v2 import inventory_repository_impl
from src.tests.lib.repositories import (
    sqlalchemy_base_repository_impl_test,
    sqlalchemy_mock_builder,
)
from src.tests.utils.fixtures import mapping_orm_fixtures


class InventoryRepositoryImplTestCase(
    sqlalchemy_base_repository_impl_test.SqlAlchemyBaseRepositoryTestCase
):
    def after_base_setup(self):
        self.inventory_repository = inventory_repository_impl.InventoryRepositoryImpl()

    def test_add_inventory_successfully(self):
        inventory_1 = mapping_orm_fixtures.build_inventory(
            name="inventory_1", entity_status=audit.Status.ACTIVE.value, create_by=1
        )

        self.inventory_repository.add(inventory_1)
        self.inventory_repository.session.add.assert_called_with(inventory_1)

    def test_get_inventory_successfully(self):
        inventory_1 = mapping_orm_fixtures.build_inventory(
            name="inventory_1", entity_status=audit.Status.ACTIVE.value, create_by=1
        )

        mocked_query = (
            sqlalchemy_mock_builder.QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .filter()
            .first(return_value=inventory_1)
            .get_mocked_query()
        )
        inventory_1.id = 5
        result = self.inventory_repository.get_by_id(inventory_1.id)

        mocked_query.assert_called_with(sqlalchemy_orm_mapping.Inventory)
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left.key, "id"
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
            inventory_1.id,
        )
        self.assertEqual(
            mocked_query.return_value.filter.return_value.filter.mock_calls[0]
            .args[0]
            .left.key,
            "entity_status",
        )
        self.assertEqual(
            mocked_query.return_value.filter.return_value.filter.mock_calls[0]
            .args[0]
            .right.value,
            audit.Status.ACTIVE.value,
        )
        self.assertEqual(result, inventory_1)

    def test_get_all_inventories_successfully(self):
        inventories = mapping_orm_fixtures.build_inventories(count=4)

        mocked_query = (
            sqlalchemy_mock_builder.QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter(return_value=inventories)
            .get_mocked_query()
        )

        returned_inventories = self.inventory_repository.get_all()

        mocked_query.assert_called_with(sqlalchemy_orm_mapping.Inventory)

        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left.key,
            "entity_status",
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
            audit.Status.ACTIVE.value,
        )
        self.assertEqual(inventories, returned_inventories)

    @mock.patch("src.lib.repositories.impl_v2.inventory_repository_impl.datetime")
    def test_delete_an_inventory_successfully(self, mocked_datetime):
        inventory_1 = mapping_orm_fixtures.build_inventory(
            name="inventory_1", entity_status=audit.Status.ACTIVE.value, create_by=1
        )
        inventory_1.updated_by = 1

        mocked_query = (
            sqlalchemy_mock_builder.QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .update()
            .get_mocked_query()
        )

        inventory_1.id = 5
        self.inventory_repository.delete_by_id(inventory_1.id, inventory_1)

        mocked_query.assert_called_with(sqlalchemy_orm_mapping.Inventory)

        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left.key,
            "id",
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
            inventory_1.id,
        )

        mocked_query.return_value.filter.return_value.update.assert_called_with(
            {
                sqlalchemy_orm_mapping.Inventory.entity_status: audit.Status.DELETED.value,
                sqlalchemy_orm_mapping.Inventory.updated_date: mocked_datetime.now(),
                sqlalchemy_orm_mapping.Inventory.updated_by: inventory_1.updated_by,
            }
        )

    def test_update_inventory_successfully(self):
        inventory_1 = mapping_orm_fixtures.build_inventory(
            name="inventory_1", entity_status=audit.Status.ACTIVE.value, create_by=1
        )
        inventory_1.id = 5
        inventory_to_be_updated = mapping_orm_fixtures.build_inventory()
        mocked_query = (
            sqlalchemy_mock_builder.QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .first(return_value=inventory_to_be_updated)
            .get_mocked_query()
        )

        self.inventory_repository.update_by_id(inventory_1.id, inventory_1)

        mocked_query.assert_called_with(sqlalchemy_orm_mapping.Inventory)

        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left.key,
            "id",
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
            inventory_1.id,
        )

        self.inventory_repository.session.add.assert_called_with(
            inventory_to_be_updated
        )
