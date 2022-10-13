from injector import Module, inject

from src.lib.repositories.impl_v2.product_repository_impl import ProductRepositoryImpl


class ProductController(Module):
    @inject
    def __init__(self, product_repository: ProductRepositoryImpl):
        self._product_repository = product_repository  # productRepository

    def add(self, product):
        self._product_repository.add(product)

    def get_by_id(self, product_id):
        return self._product_repository.get_by_id(product_id)

    def get_all(self):
        return self._product_repository.get_all()

    def delete_by_id(self, product_id, product):
        self._product_repository.delete_by_id(product_id, product)

    def update_by_id(self, product_id, product):
        self._product_repository.update_by_id(product_id, product)
