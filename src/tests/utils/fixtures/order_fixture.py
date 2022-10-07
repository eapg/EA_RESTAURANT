from src.constants.audit import Status
from src.constants.order_status import OrderStatus
from src.lib.entities.order import Order


def build_order(
    order_id=None,
    status=None,
    assigned_chef_id=None,
    entity_status=None,
    create_by=None,
):

    order = Order()
    order.id = order_id
    order.status = status or OrderStatus.NEW_ORDER
    order.assigned_chef_id = assigned_chef_id
    order.entity_status = entity_status or Status.ACTIVE
    order.create_by = create_by

    return order


def build_orders(count=1):
    return [build_order(order_id=n) for n in range(count)]
