from unittest import mock

from src.constants.audit import Status
from src.lib.entities.sqlalchemy_orm_mapping import Ingredient
from src.lib.repositories.impl_v2.ingredient_repository_impl import (
    IngredientRepositoryImpl,
)
from src.tests.lib.repositories.sqlalchemy_base_repository_impl_test import (
    SqlAlchemyBaseRepositoryTestCase,
)
from src.tests.lib.repositories.sqlalchemy_mock_builder import QueryMock
from src.tests.utils.fixtures.mapping_orm_fixtures import (
    build_ingredient,
    build_ingredients,
)


class IngredientRepositoryImplTestCase(SqlAlchemyBaseRepositoryTestCase):
    def after_base_setup(self):
        self.ingredient_repository = IngredientRepositoryImpl()

    def test_add_ingredient_successfully(self):
        ingredient_1 = build_ingredient(
            name="ingredient_1", entity_status=Status.ACTIVE.value, create_by=1
        )

        self.ingredient_repository.add(ingredient_1)
        self.ingredient_repository.session.add.assert_called_with(ingredient_1)

    def test_get_ingredient_successfully(self):
        ingredient_1 = build_ingredient(
            name="ingredient_1", entity_status=Status.ACTIVE.value, create_by=1
        )

        mocked_query = (
            QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .filter()
            .first(return_value=ingredient_1)
            .get_mocked_query()
        )
        ingredient_1.id = 5
        result = self.ingredient_repository.get_by_id(ingredient_1.id)

        mocked_query.assert_called_with(Ingredient)
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left.key, "id"
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
            ingredient_1.id,
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
        self.assertEqual(result, ingredient_1)

    def test_get_all_ingredients_successfully(self):
        ingredients = build_ingredients(count=4)

        mocked_query = (
            QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter(return_value=ingredients)
            .get_mocked_query()
        )

        returned_ingredients = self.ingredient_repository.get_all()

        mocked_query.assert_called_with(Ingredient)

        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left.key,
            "entity_status",
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
            Status.ACTIVE.value,
        )
        self.assertEqual(ingredients, returned_ingredients)

    @mock.patch("src.lib.repositories.impl_v2.ingredient_repository_impl.datetime")
    def test_delete_an_ingredient_successfully(self, mocked_datetime):
        ingredient_1 = build_ingredient(
            name="ingredient_1", entity_status=Status.ACTIVE.value, create_by=1
        )
        ingredient_1.updated_by = 1

        mocked_query = (
            QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .update()
            .get_mocked_query()
        )

        ingredient_1.id = 5
        self.ingredient_repository.delete_by_id(ingredient_1.id, ingredient_1)

        mocked_query.assert_called_with(Ingredient)

        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left.key,
            "id",
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
            ingredient_1.id,
        )

        mocked_query.return_value.filter.return_value.update.assert_called_with(
            {
                Ingredient.entity_status: Status.DELETED.value,
                Ingredient.updated_date: mocked_datetime.now(),
                Ingredient.updated_by: ingredient_1.updated_by,
            }
        )

    def test_update_ingredient_successfully(self):
        ingredient_1 = build_ingredient(
            name="ingredient_1", entity_status=Status.ACTIVE.value, create_by=1
        )
        ingredient_1.id = 5
        ingredient_to_be_updated = build_ingredient()
        mocked_query = (
            QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .first(return_value=ingredient_to_be_updated)
            .get_mocked_query()
        )

        self.ingredient_repository.update_by_id(ingredient_1.id, ingredient_1)

        mocked_query.assert_called_with(Ingredient)

        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left.key,
            "id",
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
            ingredient_1.id,
        )

        self.ingredient_repository.session.add.assert_called_with(
            ingredient_to_be_updated
        )
