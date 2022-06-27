from src.lib.entities.product_ingredient import ProductIngredient
from src.constants.audit import Status


def build_product_ingredient(
    product_ingredient_id=None,
    product_id=None,
    ingredient_id=None,
    quantity=None,
    ingredient_type=None,
    entity_status=None,
):
    product_ingredient = ProductIngredient()
    product_ingredient.id = product_ingredient_id
    product_ingredient.product_id = product_id
    product_ingredient.ingredient_id = ingredient_id
    product_ingredient.quantity = quantity
    product_ingredient.ingredient_type = ingredient_type
    product_ingredient.entity_status = entity_status or Status.ACTIVE
    return product_ingredient


def build_product_ingredients(count=1):
    return [
        build_product_ingredient(product_ingredient_id=n, quantity=None)
        for n in range(count)
    ]
