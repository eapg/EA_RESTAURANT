import unittest

from src.constants import audit
from src.lib.repositories.impl import product_ingredient_repository_impl
from src.tests.utils.fixtures import (
    ingredient_fixture,
    product_fixture,
    product_ingredient_fixture,
)


class ProductIngredientRepositoryImplTestCase(unittest.TestCase):
    def test_add_product_ingredient_successfully(self):
        product_ingredient = product_ingredient_fixture.build_product_ingredient()
        product_ingredient_repository = (
            product_ingredient_repository_impl.ProductIngredientRepositoryImpl()
        )

        product_ingredient_repository.add(product_ingredient)

        self.assertEqual(product_ingredient.id, 1)

    def test_get_product_ingredient_successfully(self):
        product_ingredients = product_ingredient_fixture.build_product_ingredients(
            count=3
        )

        product_ingredient_repository = (
            product_ingredient_repository_impl.ProductIngredientRepositoryImpl()
        )

        product_ingredient_repository.add(product_ingredients[0])
        product_ingredient_repository.add(product_ingredients[1])
        product_ingredient_repository.add(product_ingredients[2])

        found_product_ingredient3 = product_ingredient_repository.get_by_id(3)

        self.assertEqual(found_product_ingredient3.id, 3)

    def test_get_throws_key_error_for_non_existing_product_ingredient(self):
        product_ingredient1 = product_ingredient_fixture.build_product_ingredient()

        product_ingredient_repository = (
            product_ingredient_repository_impl.ProductIngredientRepositoryImpl()
        )

        product_ingredient_repository.add(product_ingredient1)

        self.assertRaises(KeyError, product_ingredient_repository.get_by_id, 2)

    def test_get_all_product_ingredients_successfully(self):
        product_ingredients_to_insert = (
            product_ingredient_fixture.build_product_ingredients(count=5)
        )

        product_ingredient_repository = (
            product_ingredient_repository_impl.ProductIngredientRepositoryImpl()
        )

        product_ingredient_repository.add(product_ingredients_to_insert[0])
        product_ingredient_repository.add(product_ingredients_to_insert[1])
        product_ingredient_repository.add(product_ingredients_to_insert[2])
        product_ingredient_repository.add(product_ingredients_to_insert[3])
        product_ingredient_repository.add(product_ingredients_to_insert[4])

        product_ingredients = product_ingredient_repository.get_all()

        self.assertEqual(
            product_ingredients,
            [
                product_ingredients_to_insert[0],
                product_ingredients_to_insert[1],
                product_ingredients_to_insert[2],
                product_ingredients_to_insert[3],
                product_ingredients_to_insert[4],
            ],
        )

    def test_get_all_product_ingredients_empty_successfully(self):
        product_ingredient_repository = (
            product_ingredient_repository_impl.ProductIngredientRepositoryImpl()
        )

        product_ingredients = product_ingredient_repository.get_all()

        self.assertEqual(product_ingredients, [])

    def test_delete_an_product_ingredient_successfully(self):
        product_ingredients_to_insert = (
            product_ingredient_fixture.build_product_ingredients(count=3)
        )
        product_ingredient_to_delete = (
            product_ingredient_fixture.build_product_ingredient(
                entity_status=audit.Status.DELETED
            )
        )
        product_ingredient_repository = (
            product_ingredient_repository_impl.ProductIngredientRepositoryImpl()
        )

        product_ingredient_repository.add(product_ingredients_to_insert[0])
        product_ingredient_repository.add(product_ingredients_to_insert[1])
        product_ingredient_repository.add(product_ingredients_to_insert[2])

        product_ingredient_repository.delete_by_id(2, product_ingredient_to_delete)

        product_ingredients = product_ingredient_repository.get_all()

        self.assertEqual(
            product_ingredients,
            [product_ingredients_to_insert[0], product_ingredients_to_insert[2]],
        )

    def test_delete_throws_key_error_when_there_are_no_product_ingredients(self):
        product_ingredient_repository = (
            product_ingredient_repository_impl.ProductIngredientRepositoryImpl()
        )
        product_ingredient_to_delete = product_fixture.build_product(
            entity_status=audit.Status.DELETED
        )
        self.assertRaises(
            KeyError,
            product_ingredient_repository.delete_by_id,
            2,
            product_ingredient_to_delete,
        )

    def test_update_product_ingredient_successfully(self):
        product_ingredients_to_insert = (
            product_ingredient_fixture.build_product_ingredients(count=2)
        )

        product_ingredient_repository = (
            product_ingredient_repository_impl.ProductIngredientRepositoryImpl()
        )

        product_ingredient_repository.add(product_ingredients_to_insert[0])
        product_ingredient_repository.add(product_ingredients_to_insert[1])

        product_ingredient_to_update = (
            product_ingredient_fixture.build_product_ingredient(quantity=10)
        )

        product_ingredient_repository.update_by_id(2, product_ingredient_to_update)
        updated_product_ingredient = product_ingredient_repository.get_by_id(2)
        product_ingredients = product_ingredient_repository.get_all()

        self.assertEqual(len(product_ingredients), 2)
        self.assertEqual(
            updated_product_ingredient.quantity, product_ingredient_to_update.quantity
        )

    def test_get_by_product_id_successfully(self):
        product_ingredient_repository = (
            product_ingredient_repository_impl.ProductIngredientRepositoryImpl()
        )
        ingredient_1 = ingredient_fixture.build_ingredient(
            ingredient_id=1, name="test ingredient"
        )
        product_1 = product_fixture.build_product(product_id=1, name="test product")
        product_ingredient_1 = product_ingredient_fixture.build_product_ingredient(
            ingredient_id=ingredient_1.id, product_id=product_1.id
        )
        product_ingredient_2 = product_ingredient_fixture.build_product_ingredient()
        product_ingredient_repository.add(product_ingredient_1)
        product_ingredient_repository.add(product_ingredient_2)

        product_ingredient_returned = product_ingredient_repository.get_by_product_id(
            product_1.id
        )
        self.assertEqual(product_ingredient_1, product_ingredient_returned[0])
