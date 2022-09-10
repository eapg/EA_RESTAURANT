from unittest import mock

from src.api.controllers.ingredient_controller import IngredientController
from src.constants.audit import Status
from src.lib.repositories.impl_v2.ingredient_repository_impl import (
    IngredientRepositoryImpl,
)

from src.tests.utils.fixtures.mapping_orm_fixtures import (
    build_ingredient,
    build_ingredients,
)
from src.tests.lib.repositories.sqlalchemy_base_repository_impl_test import (
    SqlAlchemyBaseRepositoryTestCase,
)


class IngredientRepositoryControllerIntegrationTestCase(
    SqlAlchemyBaseRepositoryTestCase
):
    def after_base_setup(self):

        self.ingredient_repository = mock.Mock(
            wraps=IngredientRepositoryImpl(self.mocked_sqlalchemy_session)
        )
        self.ingredient_controller = IngredientController(self.ingredient_repository)

    def test_add_ingredient_to_repository_using_controller(self):
        ingredient = build_ingredient()

        self.ingredient_controller.add(ingredient)
        self.ingredient_repository.add.assert_called_with(ingredient)

    def test_get_ingredient_from_repository_using_controller(self):
        ingredients = build_ingredients(count=3)

        self.ingredient_controller.add(ingredients[0])
        self.ingredient_controller.add(ingredients[1])
        self.ingredient_controller.add(ingredients[2])
        self.ingredient_repository.get_by_id.return_value = ingredients[1]
        found_ingredient1 = self.ingredient_controller.get_by_id(1)

        self.ingredient_repository.get_by_id.assert_called_with(1)
        self.assertEqual(found_ingredient1.id, 1)

    def test_get_all_ingredients_from_repository_using_controller(self):

        ingredients_to_insert = build_ingredients(count=4)

        self.ingredient_controller.add(ingredients_to_insert[0])
        self.ingredient_controller.add(ingredients_to_insert[1])
        self.ingredient_controller.add(ingredients_to_insert[2])
        self.ingredient_controller.add(ingredients_to_insert[3])
        self.ingredient_repository.get_all.return_value = ingredients_to_insert
        ingredients = self.ingredient_controller.get_all()

        self.ingredient_repository.get_all.assert_called_with()

        self.assertEqual(
            ingredients,
            [
                ingredients_to_insert[0],
                ingredients_to_insert[1],
                ingredients_to_insert[2],
                ingredients_to_insert[3],
            ],
        )

    def test_get_all_ingredients_empty_from_repository_through_controller(self):
        self.ingredient_repository.get_all.return_value = []
        ingredients = self.ingredient_controller.get_all()
        self.ingredient_repository.get_all.assert_called_with()
        self.assertEqual(ingredients, [])

    def test_delete_an_ingredient_from_repository_using_controller(self):
        ingredients_to_insert = build_ingredients(count=4)
        ingredient_to_delete = build_ingredient(entity_status=Status.DELETED)
        self.ingredient_controller.add(ingredients_to_insert[0])
        self.ingredient_controller.add(ingredients_to_insert[1])
        self.ingredient_controller.add(ingredients_to_insert[2])
        self.ingredient_controller.add(ingredients_to_insert[3])

        self.ingredient_controller.delete_by_id(3, ingredient_to_delete)
        self.ingredient_repository.get_all.return_value = [
            ingredients_to_insert[0],
            ingredients_to_insert[1],
            ingredients_to_insert[3],
        ]
        ingredients = self.ingredient_controller.get_all()

        self.ingredient_repository.delete_by_id.assert_called_once_with(
            3, ingredient_to_delete
        )

        self.assertEqual(
            ingredients,
            [
                ingredients_to_insert[0],
                ingredients_to_insert[1],
                ingredients_to_insert[3],
            ],
        )

    def test_update_ingredient_from_repository_using_controller(self):
        ingredients_to_insert = build_ingredients(count=2)

        self.ingredient_controller.add(ingredients_to_insert[0])
        self.ingredient_controller.add(ingredients_to_insert[1])

        ingredient_to_update = build_ingredient(description="updated-description")

        self.ingredient_controller.update_by_id(2, ingredient_to_update)
        self.ingredient_repository.get_by_id.return_value = ingredient_to_update
        updated_ingredient = self.ingredient_controller.get_by_id(2)
        self.ingredient_repository.get_all.return_value = ingredients_to_insert
        ingredients = self.ingredient_controller.get_all()

        self.ingredient_repository.update_by_id.assert_called_once_with(
            2, ingredient_to_update
        )

        self.assertEqual(len(ingredients), 2)
        self.assertEqual(
            updated_ingredient.description, ingredient_to_update.description
        )
