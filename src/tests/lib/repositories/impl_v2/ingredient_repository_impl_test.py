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
from src.tests.utils.test_util import (
    assert_filter_entity_status_active,
    assert_filter_id,
    assert_filter_filter_id, build_update_mock_query,
)


class IngredientRepositoryImplTestCase(SqlAlchemyBaseRepositoryTestCase):
    def after_base_setup(self):
        self.mocked_creation_session_path = mock.patch(
            "src.lib.repositories.impl_v2.ingredient_repository_impl.create_session",
            return_value=self.mocked_sqlalchemy_session,
        )
        self.ingredient_repository = IngredientRepositoryImpl(
            self.mocked_sqlalchemy_engine
        )
        self.mocked_creation_session_path.start()

    def test_add_ingredient_successfully(self):

        ingredient_1 = build_ingredient(name="ingredient_1")

        self.ingredient_repository.add(ingredient_1)
        self.mocked_sqlalchemy_session.add.assert_called_with(ingredient_1)

    def test_get_ingredient_successfully(self):

        ingredient_1 = build_ingredient(ingredient_id=1, name="ingredient_1")

        # pylint: disable=R0801
        mocked_query = (
            QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .filter()
            .first(return_value=ingredient_1)
            .get_mocked_query()
        )

        result = self.ingredient_repository.get_by_id(ingredient_1.id)

        mocked_query.assert_called_with(Ingredient)
        assert_filter_entity_status_active(self, mocked_query)
        assert_filter_filter_id(self, mocked_query)
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
        assert_filter_entity_status_active(self, mocked_query)
        self.assertEqual(ingredients, returned_ingredients)

    @mock.patch("src.lib.repositories.impl_v2.ingredient_repository_impl.datetime")
    def test_delete_an_ingredient_successfully(self, mocked_datetime):

        ingredient_1 = build_ingredient(ingredient_id=1, name="ingredient_1")
        ingredient_1.updated_by = 1

        mocked_query = build_update_mock_query(self.mocked_sqlalchemy_session)

        self.ingredient_repository.delete_by_id(ingredient_1.id, ingredient_1)

        mocked_query.assert_called_with(Ingredient)
        assert_filter_id(self, mocked_query)

        mocked_query.return_value.filter.return_value.update.assert_called_with(
            {
                Ingredient.entity_status: Status.DELETED.value,
                Ingredient.updated_date: mocked_datetime.now(),
                Ingredient.updated_by: ingredient_1.updated_by,
            }
        )

    def test_update_ingredient_successfully(self):

        ingredient_1 = build_ingredient(ingredient_id=1, name="ingredient_1")

        ingredient_to_be_updated = build_ingredient()
        mocked_query = (
            QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .first(return_value=ingredient_to_be_updated)
            .get_mocked_query()
        )

        self.ingredient_repository.update_by_id(ingredient_1.id, ingredient_1)

        assert_filter_id(self, mocked_query)
        self.mocked_sqlalchemy_session.add.assert_called_with(ingredient_to_be_updated)
