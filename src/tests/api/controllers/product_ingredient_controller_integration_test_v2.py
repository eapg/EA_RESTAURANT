from unittest import mock

from src.api.controllers.product_ingredient_controller import (
    ProductIngredientController,
)
from src.constants.audit import Status
from src.lib.repositories.impl_v2.product_ingredient_repository_impl import (
    ProductIngredientRepositoryImpl,
)

from src.tests.utils.fixtures.mapping_orm_fixtures import (
    build_product_ingredient,
    build_product_ingredients,
    build_product,
)
from src.tests.lib.repositories.sqlalchemy_base_repository_impl_test import (
    SqlAlchemyBaseRepositoryTestCase,
)


class ProductIngredientRepositoryControllerIntegrationTestCase(
    SqlAlchemyBaseRepositoryTestCase
):
    def after_base_setup(self):

        self.product_ingredient_repository = mock.Mock(
            wraps=ProductIngredientRepositoryImpl(self.mocked_sqlalchemy_session)
        )
        self.product_ingredient_controller = ProductIngredientController(
            self.product_ingredient_repository
        )

    def test_add_product_ingredient_to_repository_using_controller(self):
        product_ingredient = build_product_ingredient()

        self.product_ingredient_controller.add(product_ingredient)
        self.product_ingredient_repository.add.assert_called_with(product_ingredient)

    def test_get_product_ingredient_from_repository_using_controller(self):
        product_ingredients = build_product_ingredients(count=3)

        self.product_ingredient_controller.add(product_ingredients[0])
        self.product_ingredient_controller.add(product_ingredients[1])
        self.product_ingredient_controller.add(product_ingredients[2])
        self.product_ingredient_repository.get_by_id.return_value = product_ingredients[
            1
        ]
        found_product_ingredient1 = self.product_ingredient_controller.get_by_id(1)

        self.product_ingredient_repository.get_by_id.assert_called_with(1)
        self.assertEqual(found_product_ingredient1.id, 1)

    def test_get_all_product_ingredients_from_repository_using_controller(self):

        product_ingredients_to_insert = build_product_ingredients(count=4)

        self.product_ingredient_controller.add(product_ingredients_to_insert[0])
        self.product_ingredient_controller.add(product_ingredients_to_insert[1])
        self.product_ingredient_controller.add(product_ingredients_to_insert[2])
        self.product_ingredient_controller.add(product_ingredients_to_insert[3])
        self.product_ingredient_repository.get_all.return_value = (
            product_ingredients_to_insert
        )
        product_ingredients = self.product_ingredient_controller.get_all()

        self.product_ingredient_repository.get_all.assert_called_with()

        self.assertEqual(
            product_ingredients,
            [
                product_ingredients_to_insert[0],
                product_ingredients_to_insert[1],
                product_ingredients_to_insert[2],
                product_ingredients_to_insert[3],
            ],
        )

    def test_get_all_product_ingredients_empty_from_repository_through_controller(self):
        self.product_ingredient_repository.get_all.return_value = []
        product_ingredients = self.product_ingredient_controller.get_all()
        self.product_ingredient_repository.get_all.assert_called_with()
        self.assertEqual(product_ingredients, [])

    def test_delete_an_product_ingredient_from_repository_using_controller(self):
        product_ingredients_to_insert = build_product_ingredients(count=4)
        product_ingredient_to_delete = build_product_ingredient(
            entity_status=Status.DELETED
        )
        self.product_ingredient_controller.add(product_ingredients_to_insert[0])
        self.product_ingredient_controller.add(product_ingredients_to_insert[1])
        self.product_ingredient_controller.add(product_ingredients_to_insert[2])
        self.product_ingredient_controller.add(product_ingredients_to_insert[3])

        self.product_ingredient_controller.delete_by_id(3, product_ingredient_to_delete)
        self.product_ingredient_repository.get_all.return_value = [
            product_ingredients_to_insert[0],
            product_ingredients_to_insert[1],
            product_ingredients_to_insert[3],
        ]
        product_ingredients = self.product_ingredient_controller.get_all()

        self.product_ingredient_repository.delete_by_id.assert_called_once_with(
            3, product_ingredient_to_delete
        )

        self.assertEqual(
            product_ingredients,
            [
                product_ingredients_to_insert[0],
                product_ingredients_to_insert[1],
                product_ingredients_to_insert[3],
            ],
        )

    def test_update_product_ingredient_from_repository_using_controller(self):
        product_ingredients_to_insert = build_product_ingredients(count=2)

        self.product_ingredient_controller.add(product_ingredients_to_insert[0])
        self.product_ingredient_controller.add(product_ingredients_to_insert[1])

        product_ingredient_to_update = build_product_ingredient(quantity=5)

        self.product_ingredient_controller.update_by_id(2, product_ingredient_to_update)
        self.product_ingredient_repository.get_by_id.return_value = (
            product_ingredient_to_update
        )
        updated_product_ingredient = self.product_ingredient_controller.get_by_id(2)
        self.product_ingredient_repository.get_all.return_value = (
            product_ingredients_to_insert
        )
        product_ingredients = self.product_ingredient_controller.get_all()

        self.product_ingredient_repository.update_by_id.assert_called_once_with(
            2, product_ingredient_to_update
        )

        self.assertEqual(len(product_ingredients), 2)
        self.assertEqual(
            updated_product_ingredient.quantity, product_ingredient_to_update.quantity
        )

    def test_get_by_product_id_from_repository_using_controller(self):

        product_1 = build_product(product_id=1, name="test product")
        product_ingredient_1 = build_product_ingredient(product_id=product_1.id)
        product_ingredient_2 = build_product_ingredient()

        self.product_ingredient_controller.add(product_ingredient_1)
        self.product_ingredient_controller.add(product_ingredient_2)
        self.product_ingredient_repository.get_by_product_id.return_value = [
            product_ingredient_1,
            product_ingredient_2,
        ]
        product_ingredients_returned = (
            self.product_ingredient_controller.get_by_product_id(product_1.id)
        )
        self.product_ingredient_repository.get_by_product_id.assert_called_with(
            product_1.id
        )
        self.assertEqual(
            product_ingredients_returned, [product_ingredient_1, product_ingredient_2]
        )
