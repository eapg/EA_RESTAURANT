from functools import reduce


def products_qty_by_ingredients_qty_reducer(
    quantity_ingredients_result, product_ingredient, inventory_ingredient
):
    """
    Reducer function to get a list of quantity of ingredient to make a product by divided the quantity in the inventory
    divided by the quantity that the product needs
    """
    quantity_ingredients_result.append(
        inventory_ingredient[0].ingredient_quantity / product_ingredient.quantity
    )
    return quantity_ingredients_result


def products_qty_array_to_final_products_qty_map_reducer(
    final_product_qty_result, product_id, qty_ingredient_by_product_list_reducer
):

    final_product_qty_result[product_id] = min(qty_ingredient_by_product_list_reducer)

    return final_product_qty_result


def setup_products_qty_array_to_final_products_qty_map(
    get_inventory_ingredient_by_ingredient_id, get_product_ingredient_by_product_id
):
    def reduce_products_qty_by_ingredients_qty(product_id):
        return reduce(
            lambda quantity_ingredients_result, product_ingredient: products_qty_by_ingredients_qty_reducer(
                quantity_ingredients_result,
                product_ingredient,
                get_inventory_ingredient_by_ingredient_id(
                    product_ingredient.ingredient_id
                ),
            ),
            get_product_ingredient_by_product_id(product_id),
            [],
        )

    def reduce_products_qty_array_to_final_products_qty_map(product_ids):
        return reduce(
            lambda final_product_qty_result, product_id: products_qty_array_to_final_products_qty_map_reducer(
                final_product_qty_result,
                product_id,
                reduce_products_qty_by_ingredients_qty(
                    product_id,
                ),
            ),
            product_ids,
            {},
        )

    return reduce_products_qty_array_to_final_products_qty_map
