from src.lib.entities.product import Product
from src.constants.audit import Status


def build_product(product_id=None, name=None, description=None, entity_status=None, create_by=None):

    product = Product()
    product.id = product_id
    product.name = name or "testing-product"
    product.description = description or "product-description"
    product.entity_status = entity_status or Status.ACTIVE
    product.create_by = create_by

    return product


def build_products(count=1):
    return [
        build_product(name=f"testing-product{n}", description=f"testing-description{n}")
        for n in range(count)
    ]
