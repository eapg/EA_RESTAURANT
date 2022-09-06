from datetime import datetime

from src.constants import audit
from src.constants import order_status
from src.lib.entities import order_status_history


def build_order_status_history(
    id=None,
    order_id=None,
    from_time=None,
    to_time=None,
    from_status=None,
    to_status=None,
    entity_status=None,
):
    order_status_history_instance = order_status_history.OrderStatusHistory()
    order_status_history_instance.id = id
    order_status_history_instance.order_id = order_id
    order_status_history_instance.from_time = from_time or datetime.now()
    order_status_history_instance.to_time = to_time or datetime.now()
    order_status_history_instance.from_status = (
        from_status or order_status.OrderStatus.NEW_ORDER
    )
    order_status_history_instance.to_status = (
        to_status or order_status.OrderStatus.ORDER_PLACED
    )
    order_status_history_instance.entity_status = entity_status or audit.Status.ACTIVE
    return order_status_history_instance


def build_order_status_histories(count=1):
    return [build_order_status_history(id=n) for n in range(count)]
