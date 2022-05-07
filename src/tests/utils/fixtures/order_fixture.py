from src.lib.entities.order import Order


def build_order(order_id=None, order_details=None, order_status=None, assigned_chef=None):

    order = Order()
    order.id = order_id
    order.order_details = order_details or []
    order.order_status = order_status
    order.assigned_chef = assigned_chef

    return order


def build_orders(count=1):
    return [build_order(order_id=n, order_details=[]) for n in range(count)]
