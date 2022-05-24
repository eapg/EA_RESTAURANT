from src.lib.entities.product_ingredient import ProductIngredient


def build_product_ingredient(id=None, product_id=None, ingredient_id=None, quantity=None):
    product_ingredient = ProductIngredient()
    product_ingredient.id = id
    product_ingredient.product_id = product_id
    product_ingredient.ingredient_id = ingredient_id
    product_ingredient.quantity = quantity
    return product_ingredient


def build_product_ingredients(count=1):
    return [
        build_product_ingredient(
            id=n, quantity=None
        )
        for n in range(count)
    ]
