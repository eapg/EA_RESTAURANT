from unittest import mock

from src.constants import audit
from src.lib.entities import sqlalchemy_orm_mapping
from src.lib.repositories.impl_v2 import inventory_ingredient_repository_impl
from src.tests.lib.repositories import (
    sqlalchemy_base_repository_impl_test,
    sqlalchemy_mock_builder,
)
from src.tests.utils.fixtures import mapping_orm_fixtures


class InventoryIngredientRepositoryImplTestCase(
    sqlalchemy_base_repository_impl_test.SqlAlchemyBaseRepositoryTestCase
):
    def after_base_setup(self):
        self.inventory_ingredient_repository = (
            inventory_ingredient_repository_impl.InventoryIngredientRepositoryImpl()
        )

    def test_add_inventory_ingredient_successfully(self):
        inventory_ingredient_1 = mapping_orm_fixtures.build_inventory_ingredient()

        self.inventory_ingredient_repository.add(inventory_ingredient_1)
        self.inventory_ingredient_repository.session.add.assert_called_with(
            inventory_ingredient_1
        )

    def test_get_inventory_ingredient_successfully(self):
        inventory_ingredient_1 = mapping_orm_fixtures.build_inventory_ingredient()

        mocked_query = (
            sqlalchemy_mock_builder.QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .filter()
            .first(return_value=inventory_ingredient_1)
            .get_mocked_query()
        )
        inventory_ingredient_1.id = 5
        result = self.inventory_ingredient_repository.get_by_id(
            inventory_ingredient_1.id
        )

        mocked_query.assert_called_with(sqlalchemy_orm_mapping.InventoryIngredient)
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left.key, "id"
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
            inventory_ingredient_1.id,
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
        self.assertEqual(result, inventory_ingredient_1)

    def test_get_all_successfully(self):

        inventory_ingredients = mapping_orm_fixtures.build_inventory_ingredients(
            count=3
        )

        mocked_query = (
            sqlalchemy_mock_builder.QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter(return_value=inventory_ingredients)
            .get_mocked_query()
        )

        returned_inventory_ingredients = self.inventory_ingredient_repository.get_all()

        mocked_query.assert_called_with(sqlalchemy_orm_mapping.InventoryIngredient)

        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left.key,
            "entity_status",
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
            audit.Status.ACTIVE.value,
        )
        self.assertEqual(inventory_ingredients, returned_inventory_ingredients)

    @mock.patch(
        "src.lib.repositories.impl_v2.inventory_ingredient_repository_impl.datetime"
    )
    def test_delete_by_id_successfully(self, mocked_datetime):
        inventory_ingredient_1 = mapping_orm_fixtures.build_inventory_ingredient()
        inventory_ingredient_1.updated_by = 1

        mocked_query = (
            sqlalchemy_mock_builder.QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .update()
            .get_mocked_query()
        )

        inventory_ingredient_1.id = 5
        self.inventory_ingredient_repository.delete_by_id(
            inventory_ingredient_1.id, inventory_ingredient_1
        )

        mocked_query.assert_called_with(sqlalchemy_orm_mapping.InventoryIngredient)

        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left.key,
            "id",
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
            inventory_ingredient_1.id,
        )

        mocked_query.return_value.filter.return_value.update.assert_called_with(
            {
                sqlalchemy_orm_mapping.InventoryIngredient.entity_status: audit.Status.DELETED.value,
                sqlalchemy_orm_mapping.InventoryIngredient.updated_date: mocked_datetime.now(),
                sqlalchemy_orm_mapping.InventoryIngredient.updated_by: inventory_ingredient_1.updated_by,
            }
        )

    def test_update_by_id_successfully(self):
        inventory_ingredient_1 = mapping_orm_fixtures.build_inventory_ingredient()

        inventory_ingredient_to_be_updated = (
            mapping_orm_fixtures.build_inventory_ingredient()
        )
        mocked_query = (
            sqlalchemy_mock_builder.QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .first(return_value=inventory_ingredient_to_be_updated)
            .get_mocked_query()
        )

        self.inventory_ingredient_repository.update_by_id(
            inventory_ingredient_1.id, inventory_ingredient_1
        )

        mocked_query.assert_called_with(sqlalchemy_orm_mapping.InventoryIngredient)

        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left.key,
            "id",
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
            inventory_ingredient_1.id,
        )

        self.inventory_ingredient_repository.session.add.assert_called_with(
            inventory_ingredient_to_be_updated
        )

    def test_get_by_ingredient_id_successfully(self):
        ingredient_1 = sqlalchemy_orm_mapping.Ingredient()
        ingredient_1.id = 5

        inventory_ingredient_1 = mapping_orm_fixtures.build_inventory_ingredient(
            ingredient_id=ingredient_1.id
        )
        inventory_ingredient_2 = mapping_orm_fixtures.build_inventory_ingredient(
            ingredient_id=ingredient_1.id
        )

        inventory_ingredients_of_order_1 = [
            inventory_ingredient_1,
            inventory_ingredient_2,
        ]

        mocked_query = (
            sqlalchemy_mock_builder.QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .filter(return_value=inventory_ingredients_of_order_1)
            .get_mocked_query()
        )

        inventory_ingredients_returned = (
            self.inventory_ingredient_repository.get_by_ingredient_id(ingredient_1.id)
        )

        mocked_query.assert_called_with(sqlalchemy_orm_mapping.InventoryIngredient)

        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left.key,
            "entity_status",
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
            audit.Status.ACTIVE.value,
        )
        self.assertEqual(
            mocked_query.return_value.filter.return_value.filter.mock_calls[0]
            .args[0]
            .left.key,
            "ingredient_id",
        )

        self.assertEqual(
            mocked_query.return_value.filter.return_value.filter.mock_calls[0]
            .args[0]
            .right.value,
            ingredient_1.id,
        )
        self.assertEqual(
            inventory_ingredients_returned, inventory_ingredients_of_order_1
        )

    @mock.patch(
        "src.lib.repositories.impl_v2.inventory_ingredient_repository_impl.sql.func"
    )
    def test_get_final_product_qty_by_product_ids(self, mock_func):

        test_result = [(2, 6), (3, 33)]

        mocked_query = (
            sqlalchemy_mock_builder.QueryMock(self.mocked_sqlalchemy_session)
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
            sqlalchemy_orm_mapping.ProductIngredient.product_id,
            mock_func.min(
                sqlalchemy_orm_mapping.InventoryIngredient.quantity
                / sqlalchemy_orm_mapping.ProductIngredient.quantity
            ),
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right,
            sqlalchemy_orm_mapping.InventoryIngredient.ingredient_id,
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left,
            sqlalchemy_orm_mapping.ProductIngredient.ingredient_id,
        )

        self.assertEqual(
            mocked_query.return_value.filter.return_value.filter.mock_calls[0]
            .args[0]
            .left,
            sqlalchemy_orm_mapping.ProductIngredient.product_id,
        )

        self.assertEqual(
            mocked_query.return_value.filter.return_value.filter.mock_calls[0]
            .args[0]
            .right.value,
            [2, 3],
        )

        self.assertEqual(
            mocked_query.return_value.filter.return_value.filter.return_value.filter.mock_calls[
                0
            ]
            .args[0]
            .left.key,
            "entity_status",
        )

        self.assertEqual(
            mocked_query.return_value.filter.return_value.filter.return_value.filter.mock_calls[
                0
            ]
            .args[0]
            .right.value,
            audit.Status.ACTIVE.value,
        )

        self.assertEqual(
            mocked_query.return_value.filter.return_value.filter.return_value.filter.return_value.filter.mock_calls[
                0
            ]
            .args[0]
            .left.key,
            "entity_status",
        )

        self.assertEqual(
            mocked_query.return_value.filter.return_value.filter.return_value.filter.return_value.filter.mock_calls[
                0
            ]
            .args[0]
            .right.value,
            audit.Status.ACTIVE.value,
        )

        self.assertEqual(
            dict((product_id, result) for product_id, result in test_result),
            final_product_qty_by_product_ids_map,
        )
