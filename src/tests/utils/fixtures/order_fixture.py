from src.constants import audit
from src.constants import order_status
from src.lib.entities import order


def build_order(
    order_id=None,
    status=None,
    assigned_chef_id=None,
    entity_status=None,
    create_by=None,
):

    order_instance = order.Order()
    order_instance.id = order_id
    order_instance.status = status or order_status.OrderStatus.NEW_ORDER
    order_instance.assigned_chef_id = assigned_chef_id
    order_instance.entity_status = entity_status or audit.Status.ACTIVE
    order_instance.create_by = create_by

    return order_instance


def build_orders(count=1):
    return [build_order(order_id=n) for n in range(count)]
