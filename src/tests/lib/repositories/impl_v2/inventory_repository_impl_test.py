from unittest import mock

from src.constants.audit import Status
from src.lib.entities.sqlalchemy_orm_mapping import Inventory
from src.lib.repositories.impl_v2.inventory_repository_impl import (
    InventoryRepositoryImpl,
)
from src.tests.lib.repositories.sqlalchemy_base_repository_impl_test import (
    SqlAlchemyBaseRepositoryTestCase,
)
from src.tests.lib.repositories.sqlalchemy_mock_builder import QueryMock
from src.tests.utils.fixtures.mapping_orm_fixtures import (
    build_inventories,
    build_inventory,
)


class InventoryRepositoryImplTestCase(SqlAlchemyBaseRepositoryTestCase):
    def after_base_setup(self):
        self.mocked_creation_session_path = mock.patch(
            "src.lib.repositories.impl_v2.inventory_repository_impl.create_session",
            return_value=self.mocked_sqlalchemy_session,
        )
        self.inventory_repository = InventoryRepositoryImpl(
            self.mocked_sqlalchemy_engine
        )
        self.mocked_creation_session_path.start()

    def test_add_inventory_successfully(self):
        inventory_1 = build_inventory(
            name="inventory_1", entity_status=Status.ACTIVE.value, create_by=1
        )

        self.inventory_repository.add(inventory_1)
        self.mocked_sqlalchemy_session.add.assert_called_with(inventory_1)

    def test_get_inventory_successfully(self):
        inventory_1 = build_inventory(
            name="inventory_1", entity_status=Status.ACTIVE.value, create_by=1
        )

        mocked_query = (
            QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .filter()
            .first(return_value=inventory_1)
            .get_mocked_query()
        )
        inventory_1.id = 5
        result = self.inventory_repository.get_by_id(inventory_1.id)

        mocked_query.assert_called_with(Inventory)
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
            Status.ACTIVE.value,
        )
        self.assertEqual(result, inventory_1)

    def test_get_all_inventories_successfully(self):
        inventories = build_inventories(count=4)

        mocked_query = (
            QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter(return_value=inventories)
            .get_mocked_query()
        )

        returned_inventories = self.inventory_repository.get_all()

        mocked_query.assert_called_with(Inventory)

        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left.key,
            "entity_status",
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
            Status.ACTIVE.value,
        )
        self.assertEqual(inventories, returned_inventories)

    @mock.patch("src.lib.repositories.impl_v2.inventory_repository_impl.datetime")
    def test_delete_an_inventory_successfully(self, mocked_datetime):
        inventory_1 = build_inventory(
            name="inventory_1", entity_status=Status.ACTIVE.value, create_by=1
        )
        inventory_1.updated_by = 1

        mocked_query = (
            QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .update()
            .get_mocked_query()
        )

        inventory_1.id = 5
        self.inventory_repository.delete_by_id(inventory_1.id, inventory_1)

        mocked_query.assert_called_with(Inventory)

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
                Inventory.entity_status: Status.DELETED.value,
                Inventory.updated_date: mocked_datetime.now(),
                Inventory.updated_by: inventory_1.updated_by,
            }
        )

    def test_update_inventory_successfully(self):
        inventory_1 = build_inventory(
            name="inventory_1", entity_status=Status.ACTIVE.value, create_by=1
        )
        inventory_1.id = 5
        inventory_to_be_updated = build_inventory()
        mocked_query = (
            QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .first(return_value=inventory_to_be_updated)
            .get_mocked_query()
        )

        self.inventory_repository.update_by_id(inventory_1.id, inventory_1)

        mocked_query.assert_called_with(Inventory)

        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left.key,
            "id",
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
            inventory_1.id,
        )

        self.mocked_sqlalchemy_session.add.assert_called_with(inventory_to_be_updated)
