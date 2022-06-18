# reducer function to get assigned chef map
from functools import reduce


def array_chef_to_chef_assigned_orders_map_reducer(
    chef_with_assigned_orders_result, chef_id, orders
):
    """
    This function reduces an array of chefs to map of chefs to their
    assigned orders.
    """
    chef_with_assigned_orders_result[chef_id] = list(
        filter(
            (
                lambda order: order.assigned_chef_id is not None
                and order.assigned_chef_id == chef_id
            ),
            orders,
        )
    )

    return chef_with_assigned_orders_result


def order_products_validation_reducer(
    order_products_validation_result,
    order_detail,
    quantity_product_that_can_be_made_map,
):
    """
    This function will return a list that will contain true if there is availability to make a product and false
    if not, we this list we will determinate if an order can be assigned to a chef or cancelled.
    """

    if (
        quantity_product_that_can_be_made_map[order_detail.product_id]
        > order_detail.quantity
    ):
        order_products_validation_result.append(True)
    else:
        order_products_validation_result.append(False)

    return order_products_validation_result


def validated_orders_reducer(
    validated_orders_result, order, order_products_availability_validation
):

    validated_orders_result[order.id] = all(order_products_availability_validation)
    return validated_orders_result


def setup_validated_orders_map(
    get_final_product_qty_by_product_ids, get_order_details_by_order_id
):
    def reduce_order_products_availability_validation(order):
        order_details = get_order_details_by_order_id(order.id)
        product_ids = [
            order_detail.product_id
            for order_detail in get_order_details_by_order_id(order.id)
        ]
        return reduce(
            lambda order_products_validation_result, order_detail: order_products_validation_reducer(
                order_products_validation_result,
                order_detail,
                get_final_product_qty_by_product_ids(product_ids),
            ),
            order_details,
            [],
        )

    def reduce_validated_orders_map(orders_to_process):
        return reduce(
            lambda validated_orders_result, order: validated_orders_reducer(
                validated_orders_result,
                order,
                reduce_order_products_availability_validation(order),
            ),
            orders_to_process,
            {},
        )

    return reduce_validated_orders_map
