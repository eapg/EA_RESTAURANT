import unittest
from src.utils.utils import equals
from src.tests.utils.fixtures.ingredient_fixture import (
    build_ingredient,
    build_ingredients,
)


class TestUtils(unittest.TestCase):
    def test_to_compare_equals_true(self):
        ingredient1 = build_ingredient()
        ingredient2 = build_ingredient()

        self.assertTrue(equals(ingredient1, ingredient2))

    def test_to_compare_equals_false(self):
        ingredient1 = build_ingredient()
        ingredient2 = build_ingredient(ingredient_id=5, name="tomato")

        self.assertFalse(equals(ingredient1, ingredient2))