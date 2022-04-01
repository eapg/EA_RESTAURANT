# This file has the product repository

from src.lib.repositories.product_repository import ProductRepository


class ProductRepositoryImpl(ProductRepository):
    def __init__(self):
        self._products = {}
        self._current_id = 0

    def add(self, product):
        product.id = self._current_id
        self._products[product.id] = product
        self._current_id += 1

    def get_by_id(self, product_id):
        return self._products[product_id]

    def get_all(self):
        return self._products.values()

    def delete_by_id(self, product_id):
        self._products.pop(product_id)

    def update_by_id(self, product_id, product):
        current_product = self.get_by_id(product_id)
        current_product.name = product.name or current_product.name
        current_product.description = product.description or current_product.description
