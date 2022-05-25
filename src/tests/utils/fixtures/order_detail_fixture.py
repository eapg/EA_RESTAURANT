from src.lib.entities.order_detail import OrderDetail


def build_order_detail(
    order_detail_id=None, order_id=None, product_id=None, quantity=None
):

    order_detail_product = OrderDetail()
    order_detail_product.id = order_detail_id
    order_detail_product.order_id = order_id
    order_detail_product.product_id = product_id
    order_detail_product.quantity = quantity

    return order_detail_product


def build_order_details(count=1):
    return [build_order_detail(order_detail_id=n) for n in range(count)]
