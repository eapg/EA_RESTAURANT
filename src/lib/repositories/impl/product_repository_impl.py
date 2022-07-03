# This file has the product repository
from datetime import datetime
from src.constants.audit import Status

from src.lib.repositories.product_repository import ProductRepository


class ProductRepositoryImpl(ProductRepository):
    def __init__(self):
        self._products = {}
        self._current_id = 1

    def add(self, product):
        product.id = self._current_id
        product.create_date = datetime.now()
        product.update_by = product.create_by
        product.update_date = product.create_date
        self._products[product.id] = product
        self._current_id += 1

    def get_by_id(self, product_id):
        product_to_return = self._products[product_id]
        product_filtered = list(
            filter(
                lambda product: product.entity_status == Status.ACTIVE,
                [product_to_return],
            )
        )
        return product_filtered[0]

    def get_all(self):
        products = list(self._products.values())
        products_filtered = list(
            filter(lambda product: product.entity_status == Status.ACTIVE, products)
        )
        return list(products_filtered)

    def delete_by_id(self, product_id, product):
        product_to_be_delete = self.get_by_id(product_id)
        product_to_be_delete.entity_status = Status.DELETED
        product_to_be_delete.update_date = datetime.now()
        product_to_be_delete.update_by = product.update_by
        self._update_by_id(
            product_id, product_to_be_delete, use_merge_with_existing=False
        )

    def update_by_id(self, product_id, product):

        self._update_by_id(product_id, product)

    def _update_by_id(self, product_id, product, use_merge_with_existing=True):

        current_product = self.get_by_id(product_id) if use_merge_with_existing else product
        current_product.name = product.name or current_product.name
        current_product.description = (
            product.description or current_product.description
        )
        current_product.update_date = datetime.now()
        current_product.update_by = product.update_by or current_product.update_by
        current_product.entity_status = (
            product.entity_status or current_product.entity_status
        )
