import unittest

from src.lib.repositories.impl.product_ingredient_repository_impl import ProductIngredientRepositoryImpl
from src.tests.utils.fixtures.product_ingredient_fixture import build_product_ingredient, build_product_ingredients


class ProductIngredientRepositoryImplTestCase(unittest.TestCase):
    def test_add_product_ingredient_successfully(self):
        product_ingredient = build_product_ingredient()
        product_ingredient_repository = ProductIngredientRepositoryImpl()

        self.assertIsNone(product_ingredient.id)

        product_ingredient_repository.add(product_ingredient)

        self.assertEqual(product_ingredient.id, 1)

    def test_get_product_ingredient_successfully(self):
        product_ingredients = build_product_ingredients(count=3)

        product_ingredient_repository = ProductIngredientRepositoryImpl()

        product_ingredient_repository.add(product_ingredients[0])
        product_ingredient_repository.add(product_ingredients[1])
        product_ingredient_repository.add(product_ingredients[2])

        found_product_ingredient3 = product_ingredient_repository.get_by_id(3)

        self.assertEqual(found_product_ingredient3.id, 3)

    def test_get_throws_key_error_for_non_existing_product_ingredient(self):
        product_ingredient1 = build_product_ingredient()

        product_ingredient_repository = ProductIngredientRepositoryImpl()

        product_ingredient_repository.add(product_ingredient1)

        self.assertRaises(KeyError, product_ingredient_repository.get_by_id, 2)

    def test_get_all_product_ingredients_successfully(self):
        product_ingredients_to_insert = build_product_ingredients(count=5)

        product_ingredient_repository = ProductIngredientRepositoryImpl()

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
        product_ingredient_repository = ProductIngredientRepositoryImpl()

        product_ingredients = product_ingredient_repository.get_all()

        self.assertEqual(product_ingredients, [])

    def test_delete_an_product_ingredient_successfully(self):
        product_ingredients_to_insert = build_product_ingredients(count=3)

        product_ingredient_repository = ProductIngredientRepositoryImpl()

        product_ingredient_repository.add(product_ingredients_to_insert[0])
        product_ingredient_repository.add(product_ingredients_to_insert[1])
        product_ingredient_repository.add(product_ingredients_to_insert[2])

        product_ingredient_repository.delete_by_id(2)

        product_ingredients = product_ingredient_repository.get_all()

        self.assertEqual(product_ingredients, [product_ingredients_to_insert[0], product_ingredients_to_insert[2]])

    def test_delete_throws_key_error_when_there_are_no_product_ingredients(self):
        product_ingredient_repository = ProductIngredientRepositoryImpl()

        self.assertRaises(KeyError, product_ingredient_repository.delete_by_id, 2)

    def test_update_product_ingredient_successfully(self):
        product_ingredients_to_insert = build_product_ingredients(count=2)

        product_ingredient_repository = ProductIngredientRepositoryImpl()

        product_ingredient_repository.add(product_ingredients_to_insert[0])
        product_ingredient_repository.add(product_ingredients_to_insert[1])

        product_ingredient_to_update = build_product_ingredient(quantity=10)

        product_ingredient_repository.update_by_id(2, product_ingredient_to_update)
        updated_product_ingredient = product_ingredient_repository.get_by_id(2)
        product_ingredients = product_ingredient_repository.get_all()

        self.assertEqual(len(product_ingredients), 2)
        self.assertEqual(updated_product_ingredient.quantity, product_ingredient_to_update.quantity)