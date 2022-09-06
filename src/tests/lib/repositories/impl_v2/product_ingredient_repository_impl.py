from unittest import mock

from src.constants import audit
from src.lib.entities import sqlalchemy_orm_mapping
from src.lib.repositories.impl_v2 import product_ingredient_repository_impl
from src.tests.lib.repositories import (
    sqlalchemy_base_repository_impl_test,
    sqlalchemy_mock_builder,
)
from src.tests.utils.fixtures import mapping_orm_fixtures


class ProductIngredientRepositoryImplTestCase(
    sqlalchemy_base_repository_impl_test.SqlAlchemyBaseRepositoryTestCase
):
    def after_base_setup(self):
        self.product_ingredient_repository = (
            product_ingredient_repository_impl.ProductIngredientRepositoryImpl()
        )

    def test_add_product_ingredient_successfully(self):
        product_ingredient_1 = mapping_orm_fixtures.build_product_ingredient()

        self.product_ingredient_repository.add(product_ingredient_1)
        self.product_ingredient_repository.session.add.assert_called_with(
            product_ingredient_1
        )

    def test_get_product_ingredient_successfully(self):
        product_ingredient_1 = mapping_orm_fixtures.build_product_ingredient()

        mocked_query = (
            sqlalchemy_mock_builder.QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .filter()
            .first(return_value=product_ingredient_1)
            .get_mocked_query()
        )
        product_ingredient_1.id = 5
        result = self.product_ingredient_repository.get_by_id(product_ingredient_1.id)

        mocked_query.assert_called_with(sqlalchemy_orm_mapping.ProductIngredient)
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left.key, "id"
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
            product_ingredient_1.id,
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
        self.assertEqual(result, product_ingredient_1)

    def test_get_all_product_ingredients_successfully(self):
        product_ingredients = mapping_orm_fixtures.build_product_ingredients(count=4)

        mocked_query = (
            sqlalchemy_mock_builder.QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter(return_value=product_ingredients)
            .get_mocked_query()
        )

        returned_product_ingredients = self.product_ingredient_repository.get_all()

        mocked_query.assert_called_with(sqlalchemy_orm_mapping.ProductIngredient)

        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left.key,
            "entity_status",
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
            audit.Status.ACTIVE.value,
        )
        self.assertEqual(product_ingredients, returned_product_ingredients)

    @mock.patch(
        "src.lib.repositories.impl_v2.product_ingredient_repository_impl.datetime"
    )
    def test_delete_an_product_ingredient_successfully(self, mocked_datetime):
        product_ingredient_1 = mapping_orm_fixtures.build_product_ingredient()
        product_ingredient_1.updated_by = 1

        mocked_query = (
            sqlalchemy_mock_builder.QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .update()
            .get_mocked_query()
        )

        product_ingredient_1.id = 5
        self.product_ingredient_repository.delete_by_id(
            product_ingredient_1.id, product_ingredient_1
        )

        mocked_query.assert_called_with(sqlalchemy_orm_mapping.ProductIngredient)

        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left.key,
            "id",
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
            product_ingredient_1.id,
        )

        mocked_query.return_value.filter.return_value.update.assert_called_with(
            {
                sqlalchemy_orm_mapping.ProductIngredient.entity_status: audit.Status.DELETED.value,
                sqlalchemy_orm_mapping.ProductIngredient.updated_date: mocked_datetime.now(),
                sqlalchemy_orm_mapping.ProductIngredient.updated_by: product_ingredient_1.updated_by,
            }
        )

    def test_update_product_ingredient_successfully(self):
        product_ingredient_1 = mapping_orm_fixtures.build_product_ingredient()
        product_ingredient_1.id = 5
        product_ingredient_to_be_updated = (
            mapping_orm_fixtures.build_product_ingredient()
        )
        mocked_query = (
            sqlalchemy_mock_builder.QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .first(return_value=product_ingredient_to_be_updated)
            .get_mocked_query()
        )

        self.product_ingredient_repository.update_by_id(
            product_ingredient_1.id, product_ingredient_1
        )

        mocked_query.assert_called_with(sqlalchemy_orm_mapping.ProductIngredient)

        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left.key,
            "id",
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
            product_ingredient_1.id,
        )

        self.product_ingredient_repository.session.add.assert_called_with(
            product_ingredient_to_be_updated
        )

    def test_get_by_product_id_successfully(self):
        product_1 = sqlalchemy_orm_mapping.Product()
        product_1.id = 5
        product_ingredient_1 = mapping_orm_fixtures.build_product_ingredient(
            product_id=product_1.id
        )
        product_ingredient_2 = mapping_orm_fixtures.build_product_ingredient(
            product_id=product_1.id
        )

        product_ingredients_of_order_1 = [product_ingredient_1, product_ingredient_2]

        mocked_query = (
            sqlalchemy_mock_builder.QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .filter(return_value=product_ingredients_of_order_1)
            .get_mocked_query()
        )

        product_ingredients_returned = (
            self.product_ingredient_repository.get_by_product_id(product_1.id)
        )

        mocked_query.assert_called_with(sqlalchemy_orm_mapping.ProductIngredient)

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
            "product_id",
        )

        self.assertEqual(
            mocked_query.return_value.filter.return_value.filter.mock_calls[0]
            .args[0]
            .right.value,
            product_1.id,
        )
        self.assertEqual(product_ingredients_returned, product_ingredients_of_order_1)
