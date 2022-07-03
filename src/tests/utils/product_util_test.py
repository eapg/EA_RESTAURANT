import unittest
from src.tests.utils.fixtures import (
    ingredient_fixture,
    product_fixture,
    chef_fixture,
)
from src.constants.cooking_type import CookingType
from src.utils import product_util


class ProductUtil(unittest.TestCase):
    def test_product_preparation_time(self):
        ingredient_cheese = ingredient_fixture.build_ingredient(
            name="cheese",
            description="cheddar cheese",
            ingredient_type=CookingType.ADDING, # 2 minutes
        )
        ingredient_bread = ingredient_fixture.build_ingredient(
            name="bread",
            description="italian bread",
            ingredient_type=CookingType.ROASTING, # 3 minutes
        )
        ingredient_tomato = ingredient_fixture.build_ingredient(
            name="tomato", description="roma tomato", ingredient_type=CookingType.ADDING # 2 minutes
        )
        ingredient_meat = ingredient_fixture.build_ingredient(
            name="meat",
            description="hamburger meat",
            ingredient_type=CookingType.FRYING, # 5 minutes
        )
        ingredient_bacon = ingredient_fixture.build_ingredient(
            name="bacon", description="bacon", ingredient_type=CookingType.ADDING # 2 minutes
        )

        product_hamburger = product_fixture.build_product(
            name="hamburger", description="bacon cheese burger"
        )
        product_hamburger.ingredients.append(ingredient_cheese)
        product_hamburger.ingredients.append(ingredient_bread)
        product_hamburger.ingredients.append(ingredient_tomato)
        product_hamburger.ingredients.append(ingredient_meat)
        product_hamburger.ingredients.append(ingredient_bacon)

        chef_basic = chef_fixture.build_chef(name="Juan p", chef_skills=1)

        self.assertEqual(
            product_util.product_preparation_time(product_hamburger, chef_basic), 14.0
        )
