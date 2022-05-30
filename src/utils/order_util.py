# reducer function to get assigned chef map


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
