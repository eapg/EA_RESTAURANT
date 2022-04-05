from src.lib.entities.order import Order


def build_order(order_id=None, order_details=None):

    order = Order()
    order.id = order_id
    order.ingredients = order_details or []

    return order


def build_orders(count=1):
    return [build_order(order_id=n, order_details=[]) for n in range(count)]
