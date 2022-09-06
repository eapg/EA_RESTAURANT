import unittest

from src.tests.utils.fixtures import ingredient_fixture
from src.utils import utils


class TestUtils(unittest.TestCase):
    def test_to_compare_equals_true(self):
        ingredient1 = ingredient_fixture.build_ingredient()
        ingredient2 = ingredient_fixture.build_ingredient()

        self.assertTrue(utils.equals(ingredient1, ingredient2))

    def test_to_compare_equals_false(self):
        ingredient1 = ingredient_fixture.build_ingredient()
        ingredient2 = ingredient_fixture.build_ingredient(
            ingredient_id=5, name="tomato"
        )

        self.assertFalse(utils.equals(ingredient1, ingredient2))
