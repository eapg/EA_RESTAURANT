from src.constants import audit
from src.lib.entities import product_ingredient


def build_product_ingredient(
    product_ingredient_id=None,
    product_id=None,
    ingredient_id=None,
    quantity=None,
    ingredient_type=None,
    entity_status=None,
    create_by=None,
):
    product_ingredient_instance = product_ingredient.ProductIngredient()
    product_ingredient_instance.id = product_ingredient_id
    product_ingredient_instance.product_id = product_id
    product_ingredient_instance.ingredient_id = ingredient_id
    product_ingredient_instance.quantity = quantity
    product_ingredient_instance.ingredient_type = ingredient_type
    product_ingredient_instance.entity_status = entity_status or audit.Status.ACTIVE
    product_ingredient_instance.create_by = create_by
    return product_ingredient_instance


def build_product_ingredients(count=1):
    return [
        build_product_ingredient(product_ingredient_id=n, quantity=None)
        for n in range(count)
    ]
