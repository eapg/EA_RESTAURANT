from src.constants import audit
from src.lib.entities import product


def build_product(
    product_id=None, name=None, description=None, entity_status=None, create_by=None
):

    product_instance = product.Product()
    product_instance.id = product_id
    product_instance.name = name or "testing-product"
    product_instance.description = description or "product-description"
    product_instance.entity_status = entity_status or audit.Status.ACTIVE
    product_instance.create_by = create_by

    return product_instance


def build_products(count=1):
    return [
        build_product(name=f"testing-product{n}", description=f"testing-description{n}")
        for n in range(count)
    ]
