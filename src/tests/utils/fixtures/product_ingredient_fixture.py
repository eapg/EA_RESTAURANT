from src.lib.entities.product_ingredient import ProductIngredient
from src.tests.utils.fixtures.ingredient_fixture import build_ingredient
from src.tests.utils.fixtures.product_fixture import build_product


def build_product_ingredient(id=None, product=None, ingredient=None, quantity=None):
    product_ingredient = ProductIngredient()
    product_ingredient.id = id
    product_ingredient.product = product or build_product()
    product_ingredient.ingredient = ingredient or build_ingredient()
    product_ingredient.quantity = quantity
    return product_ingredient


def build_product_ingredients(count=1):
    return [
        build_product_ingredient(
            id=n, ingredient=build_ingredient(), quantity=None
        )
        for n in range(count)
    ]
