from src.constants.audit import Status
from src.constants.order_status import OrderStatus
from src.lib.entities.mongo_engine_odm_mapping import OrderStatusHistory
from datetime import datetime


def build_order_status_history(
    order_id=None,
    from_time=None,
    from_status=None,
    to_time=None,
    to_status=None,
    entity_status=None,
    created_by=None,
    created_date=None,
    updated_by=None,
    updated_date=None,
):
    order_status_history = OrderStatusHistory()
    order_status_history.order_id = order_id or 1
    order_status_history.from_time = from_time or datetime.now()
    order_status_history.from_status = from_status or OrderStatus.NEW_ORDER.name
    order_status_history.to_time = to_time
    order_status_history.to_status = to_status
    order_status_history.entity_status = entity_status or Status.ACTIVE.value
    order_status_history.created_by = created_by or 1
    order_status_history.created_date = created_date or datetime.now()
    order_status_history.updated_by = updated_by or order_status_history.created_by
    order_status_history.updated_date = (
        updated_date or order_status_history.created_date
    )
    return order_status_history


def build_order_status_histories(count=1):
    return [build_order_status_history() for n in range(count)]
