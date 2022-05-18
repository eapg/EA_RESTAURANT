from src.lib.entities.order_status_history import OrderStatusHistory
from src.tests.utils.fixtures.order_fixture import build_order
from datetime import datetime
from src.constants.order_status import OrderStatus


def build_order_status_history(
    id=None, order=None, from_time=None, to_time=None, from_status=None, to_status=None
):
    order_status_history = OrderStatusHistory()
    order_status_history.id = id
    order_status_history.order = order or build_order()
    order_status_history.from_time = from_time or datetime.now()
    order_status_history.to_time = to_time or datetime.now()
    order_status_history.from_status = from_status or OrderStatus.NEW_ORDER
    order_status_history.to_status = to_status or OrderStatus.ORDER_PLACED
    return order_status_history


def build_order_status_histories(count=1):
    return [build_order_status_history(id=n) for n in range(count)]
