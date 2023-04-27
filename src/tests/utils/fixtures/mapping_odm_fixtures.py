from datetime import datetime

from src.constants.audit import Status
from src.constants.order_status import OrderStatus
from src.lib.entities.mongo_engine_odm_mapping import OrderStatusHistory
from src.tests.utils.fixtures.fixture_args import BaseEntityArgs

DEFAULT_BASE_ENTITY_ARGS = BaseEntityArgs()


def build_order_status_history(
    id=None, order_id=None, from_time=None, from_status=None, service=None, fixture_args=DEFAULT_BASE_ENTITY_ARGS
):
    order_status_history = OrderStatusHistory()
    order_status_history.id = id
    order_status_history.order_id = order_id or 1
    order_status_history.from_time = from_time or datetime.now()
    order_status_history.from_status = from_status or OrderStatus.NEW_ORDER.name
    order_status_history.to_time = None
    order_status_history.to_status = None
    order_status_history.service = service
    order_status_history.entity_status = (
        fixture_args.entity_status or Status.ACTIVE.value
    )
    order_status_history.created_by = fixture_args.created_by or 1
    order_status_history.created_date = fixture_args.created_date or datetime.now()
    order_status_history.updated_by = (
        fixture_args.updated_by or order_status_history.created_by
    )
    order_status_history.updated_date = (
        fixture_args.updated_date or order_status_history.created_date
    )
    return order_status_history


def build_order_status_histories(count=1):
    return [build_order_status_history() for n in range(count)]
