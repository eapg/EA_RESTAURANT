from src.constants.audit import Status
from src.lib.entities.order_detail import OrderDetail


def build_order_detail(
    order_detail_id=None,
    order_id=None,
    product_id=None,
    quantity=None,
    entity_status=None,
    create_by=None,
):

    order_detail = OrderDetail()
    order_detail.id = order_detail_id
    order_detail.order_id = order_id
    order_detail.product_id = product_id
    order_detail.quantity = quantity
    order_detail.entity_status = entity_status or Status.ACTIVE
    order_detail.create_by = create_by

    return order_detail


def build_order_details(count=1):
    return [build_order_detail(order_detail_id=n) for n in range(count)]
