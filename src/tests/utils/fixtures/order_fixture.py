from src.lib.entities.order import Order
from src.constants.order_status import OrderStatus


def build_order(order_id=None, order_details=None, status=None, assigned_chef=None):

    order = Order()
    order.id = order_id
    order.order_details = order_details or []
    order.status = status or OrderStatus.NEW_ORDER
    order.assigned_chef = assigned_chef

    return order


def build_orders(count=1):
    return [build_order(order_id=n, order_details=[]) for n in range(count)]
