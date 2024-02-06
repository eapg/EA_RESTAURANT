from unittest import mock

from src.constants.audit import Status
from src.lib.entities.sqlalchemy_orm_mapping import (
    InventoryIngredient,
    ProductIngredient,
)
from src.lib.repositories.impl_v2.inventory_ingredient_repository_impl import (
    InventoryIngredientRepositoryImpl,
)
from src.tests.lib.repositories.sqlalchemy_base_repository_impl_test import (
    SqlAlchemyBaseRepositoryTestCase,
)
from src.tests.lib.repositories.sqlalchemy_mock_builder import QueryMock

from src.tests.utils.fixtures.mapping_orm_fixtures import (
    build_inventory_ingredient,
    build_inventory_ingredients,
    build_ingredient,
)
from src.tests.utils.test_util import (
    assert_filter_id,
    assert_filter_filter_id,
    assert_filter_entity_status_active, assert_filter_filter_value_id, build_update_mock_query,
)


class InventoryIngredientRepositoryImplTestCase(SqlAlchemyBaseRepositoryTestCase):
    def after_base_setup(self):
        self.mocked_creation_session_path = mock.patch(
            "src.lib.repositories.impl_v2.inventory_ingredient_repository_impl.create_session",
            return_value=self.mocked_sqlalchemy_session,
        )
        self.inventory_ingredient_repository = InventoryIngredientRepositoryImpl(
            self.mocked_sqlalchemy_engine
        )
        self.mocked_creation_session_path.start()

    def test_add_inventory_ingredient_successfully(self):

        inventory_ingredient_1 = build_inventory_ingredient()

        self.inventory_ingredient_repository.add(inventory_ingredient_1)
        self.mocked_sqlalchemy_session.add.assert_called_with(inventory_ingredient_1)

    def test_get_inventory_ingredient_successfully(self):

        inventory_ingredient_1 = build_inventory_ingredient(inventory_ingredient_id=1)

        # pylint: disable=R0801
        mocked_query = (
            QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .filter()
            .first(return_value=inventory_ingredient_1)
            .get_mocked_query()
        )

        result = self.inventory_ingredient_repository.get_by_id(
            inventory_ingredient_1.id
        )

        mocked_query.assert_called_with(InventoryIngredient)
        assert_filter_entity_status_active(self, mocked_query)
        assert_filter_filter_id(self, mocked_query)

        self.assertEqual(result, inventory_ingredient_1)

    def test_get_all_successfully(self):

        inventory_ingredients = build_inventory_ingredients(count=3)

        mocked_query = (
            QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter(return_value=inventory_ingredients)
            .get_mocked_query()
        )

        returned_inventory_ingredients = self.inventory_ingredient_repository.get_all()

        mocked_query.assert_called_with(InventoryIngredient)
        assert_filter_entity_status_active(self, mocked_query)

        self.assertEqual(inventory_ingredients, returned_inventory_ingredients)

    @mock.patch(
        "src.lib.repositories.impl_v2.inventory_ingredient_repository_impl.datetime"
    )
    def test_delete_by_id_successfully(self, mocked_datetime):

        inventory_ingredient_1 = build_inventory_ingredient(inventory_ingredient_id=1)
        inventory_ingredient_1.updated_by = 1

        mocked_query = build_update_mock_query(self.mocked_sqlalchemy_session)

        self.inventory_ingredient_repository.delete_by_id(
            inventory_ingredient_1.id, inventory_ingredient_1
        )

        mocked_query.assert_called_with(InventoryIngredient)
        assert_filter_id(self, mocked_query)

        mocked_query.return_value.filter.return_value.update.assert_called_with(
            {
                InventoryIngredient.entity_status: Status.DELETED.value,
                InventoryIngredient.updated_date: mocked_datetime.now(),
                InventoryIngredient.updated_by: inventory_ingredient_1.updated_by,
            }
        )

    def test_update_by_id_successfully(self):

        inventory_ingredient_1 = build_inventory_ingredient()

        inventory_ingredient_to_be_updated = build_inventory_ingredient()
        mocked_query = (
            QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .first(return_value=inventory_ingredient_to_be_updated)
            .get_mocked_query()
        )

        self.inventory_ingredient_repository.update_by_id(
            inventory_ingredient_1.id, inventory_ingredient_1
        )

        mocked_query.assert_called_with(InventoryIngredient)
        assert_filter_id(self, mocked_query)

        self.mocked_sqlalchemy_session.add.assert_called_with(
            inventory_ingredient_to_be_updated
        )

    def test_get_by_ingredient_id_successfully(self):

        ingredient_1 = build_ingredient(ingredient_id=1)

        inventory_ingredient_1 = build_inventory_ingredient(
            ingredient_id=ingredient_1.id
        )
        inventory_ingredient_2 = build_inventory_ingredient(
            ingredient_id=ingredient_1.id
        )

        inventory_ingredients_of_order_1 = [
            inventory_ingredient_1,
            inventory_ingredient_2,
        ]

        mocked_query = (
            QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .filter(return_value=inventory_ingredients_of_order_1)
            .get_mocked_query()
        )

        inventory_ingredients_returned = (
            self.inventory_ingredient_repository.get_by_ingredient_id(ingredient_1.id)
        )

        mocked_query.assert_called_with(InventoryIngredient)
        assert_filter_entity_status_active(self, mocked_query)
        assert_filter_filter_value_id(self, mocked_query, value="ingredient_id")

        self.assertEqual(
            inventory_ingredients_returned, inventory_ingredients_of_order_1
        )

    @mock.patch(
        "src.lib.repositories.impl_v2.inventory_ingredient_repository_impl.func"
    )
    def test_get_final_product_qty_by_product_ids(self, mock_func):

        test_result = [(2, 6), (3, 33)]

        # pylint: disable=R0801
        mocked_query = (
            QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .filter()
            .filter()
            .filter()
            .group_by()
            .all(return_value=test_result)
            .get_mocked_query()
        )

        final_product_qty_by_product_ids_map = (
            self.inventory_ingredient_repository.get_final_product_qty_by_product_ids(
                [2, 3]
            )
        )

        mocked_query.assert_called_with(
            ProductIngredient.product_id,
            mock_func.min(InventoryIngredient.quantity / ProductIngredient.quantity),
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right,
            InventoryIngredient.ingredient_id,
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left,
            ProductIngredient.ingredient_id,
        )

        self.assertEqual(
            mocked_query.return_value.filter.return_value.filter.mock_calls[0]
            .args[0]
            .left,
            ProductIngredient.product_id,
        )

        self.assertEqual(
            mocked_query.return_value.filter.return_value.filter.mock_calls[0]
            .args[0]
            .right.value,
            [2, 3],
        )
        mocked_filter_filter = mocked_query.return_value.filter.return_value.filter

        self.assertEqual(
            mocked_filter_filter.return_value.filter.mock_calls[0].args[0].left.key,
            "entity_status",
        )

        self.assertEqual(
            mocked_filter_filter.return_value.filter.mock_calls[0].args[0].right.value,
            Status.ACTIVE.value,
        )

        self.assertEqual(
            mocked_filter_filter.return_value.filter.return_value.filter.mock_calls[0]
            .args[0]
            .left.key,
            "entity_status",
        )

        self.assertEqual(
            mocked_filter_filter.return_value.filter.return_value.filter.mock_calls[0]
            .args[0]
            .right.value,
            Status.ACTIVE.value,
        )

        self.assertEqual(
            dict((product_id, result) for product_id, result in test_result),
            final_product_qty_by_product_ids_map,
        )
