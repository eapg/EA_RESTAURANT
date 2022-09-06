from src.constants import audit
from src.lib.entities import order_detail


def build_order_detail(
    order_detail_id=None,
    order_id=None,
    product_id=None,
    quantity=None,
    entity_status=None,
    create_by=None,
):

    order_detail_instance = order_detail.OrderDetail()
    order_detail_instance.id = order_detail_id
    order_detail_instance.order_id = order_id
    order_detail_instance.product_id = product_id
    order_detail_instance.quantity = quantity
    order_detail_instance.entity_status = entity_status or audit.Status.ACTIVE
    order_detail_instance.create_by = create_by

    return order_detail_instance


def build_order_details(count=1):
    return [build_order_detail(order_detail_id=n) for n in range(count)]
