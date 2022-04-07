from src.lib.entities.order_detail import OrderDetail


def build_order_detail(order_detail_id=None, order_product_map=None):
    order_detail = OrderDetail()
    order_detail.id = order_detail_id
    order_detail.order_product_map = order_product_map or []

    return order_detail


def build_order_details(count=1):
    return [
        build_order_detail(order_detail_id=n, order_product_map=[])
        for n in range(count)
    ]
