from unittest import mock

from src.constants.audit import Status
from src.lib.entities.sqlalchemy_orm_mapping import Product, ProductIngredient
from src.lib.repositories.impl_v2.product_ingredient_repository_impl import (
    ProductIngredientRepositoryImpl,
)
from src.tests.lib.repositories.sqlalchemy_base_repository_impl_test import (
    SqlAlchemyBaseRepositoryTestCase,
)
from src.tests.lib.repositories.sqlalchemy_mock_builder import QueryMock
from src.tests.utils.fixtures.mapping_orm_fixtures import (
    build_product_ingredient,
    build_product_ingredients,
)


class ProductIngredientRepositoryImplTestCase(SqlAlchemyBaseRepositoryTestCase):
    def after_base_setup(self):
        self.mocked_creation_session_path = mock.patch(
            "src.lib.repositories.impl_v2.product_ingredient_repository_impl.create_session",
            return_value=self.mocked_sqlalchemy_session,
        )
        self.product_ingredient_repository = ProductIngredientRepositoryImpl(
            self.mocked_sqlalchemy_engine
        )
        self.mocked_creation_session_path.start()

    def test_add_product_ingredient_successfully(self):
        product_ingredient_1 = build_product_ingredient()

        self.product_ingredient_repository.add(product_ingredient_1)
        self.mocked_sqlalchemy_session.add.assert_called_with(product_ingredient_1)

    def test_get_product_ingredient_successfully(self):
        product_ingredient_1 = build_product_ingredient()

        mocked_query = (
            QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .filter()
            .first(return_value=product_ingredient_1)
            .get_mocked_query()
        )
        product_ingredient_1.id = 5
        result = self.product_ingredient_repository.get_by_id(product_ingredient_1.id)

        mocked_query.assert_called_with(ProductIngredient)
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
            Status.ACTIVE.value,
        )
        self.assertEqual(result, product_ingredient_1)

    def test_get_all_product_ingredients_successfully(self):
        product_ingredients = build_product_ingredients(count=4)

        mocked_query = (
            QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter(return_value=product_ingredients)
            .get_mocked_query()
        )

        returned_product_ingredients = self.product_ingredient_repository.get_all()

        mocked_query.assert_called_with(ProductIngredient)

        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left.key,
            "entity_status",
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
            Status.ACTIVE.value,
        )
        self.assertEqual(product_ingredients, returned_product_ingredients)

    @mock.patch(
        "src.lib.repositories.impl_v2.product_ingredient_repository_impl.datetime"
    )
    def test_delete_an_product_ingredient_successfully(self, mocked_datetime):
        product_ingredient_1 = build_product_ingredient()
        product_ingredient_1.updated_by = 1

        mocked_query = (
            QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .update()
            .get_mocked_query()
        )

        product_ingredient_1.id = 5
        self.product_ingredient_repository.delete_by_id(
            product_ingredient_1.id, product_ingredient_1
        )

        mocked_query.assert_called_with(ProductIngredient)

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
                ProductIngredient.entity_status: Status.DELETED.value,
                ProductIngredient.updated_date: mocked_datetime.now(),
                ProductIngredient.updated_by: product_ingredient_1.updated_by,
            }
        )

    def test_update_product_ingredient_successfully(self):
        product_ingredient_1 = build_product_ingredient()
        product_ingredient_1.id = 5
        product_ingredient_to_be_updated = build_product_ingredient()
        mocked_query = (
            QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .first(return_value=product_ingredient_to_be_updated)
            .get_mocked_query()
        )

        self.product_ingredient_repository.update_by_id(
            product_ingredient_1.id, product_ingredient_1
        )

        mocked_query.assert_called_with(ProductIngredient)

        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left.key,
            "id",
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
            product_ingredient_1.id,
        )

        self.mocked_sqlalchemy_session.add.assert_called_with(
            product_ingredient_to_be_updated
        )

    def test_get_by_product_id_successfully(self):
        product_1 = Product()
        product_1.id = 5
        product_ingredient_1 = build_product_ingredient(product_id=product_1.id)
        product_ingredient_2 = build_product_ingredient(product_id=product_1.id)

        product_ingredients_of_order_1 = [product_ingredient_1, product_ingredient_2]

        mocked_query = (
            QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .filter(return_value=product_ingredients_of_order_1)
            .get_mocked_query()
        )

        product_ingredients_returned = (
            self.product_ingredient_repository.get_by_product_id(product_1.id)
        )

        mocked_query.assert_called_with(ProductIngredient)

        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left.key,
            "entity_status",
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
            Status.ACTIVE.value,
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
