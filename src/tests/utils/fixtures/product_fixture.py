from src.lib.entities.product import Product


def build_product(product_id=None, name=None, description=None):

    product = Product()
    product.id = product_id
    product.name = name or "testing-product"
    product.description = description or "product-description"

    return product


def build_products(count=1):
    return [
        build_product(name=f"testing-product{n}", description=f"testing-description{n}")
        for n in range(count)
    ]
