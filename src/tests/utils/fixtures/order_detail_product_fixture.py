from src.lib.entities.order_detail_product import OrderDetailProduct
from src.tests.utils.fixtures.product_fixture import build_product


def build_order_detail_product(
    order_detail_product_id=None, order_detail_id=None, product=None, quantity=None
):

    order_detail_product = OrderDetailProduct()
    order_detail_product.id = order_detail_product_id
    order_detail_product.order_detail_id = order_detail_id
    order_detail_product.product = product or build_product()
    order_detail_product.quantity = quantity

    return order_detail_product


def build_order_detail_products(count=1):
    return [build_order_detail_product(order_detail_product_id=n) for n in range(count)]
