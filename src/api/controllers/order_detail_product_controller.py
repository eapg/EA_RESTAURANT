class OrderDetailProductController:
    def __init__(self, order_detail_product_repository):
        self._order_detail_product_repository = (
            order_detail_product_repository  # order_detail_productRepository
        )

    def add(self, order_detail_product):
        self._order_detail_product_repository.add(order_detail_product)

    def get_by_id(self, order_detail_product_id):
        return self._order_detail_product_repository.get_by_id(order_detail_product_id)

    def get_all(self):
        return self._order_detail_product_repository.get_all()

    def delete_by_id(self, order_detail_product_id):
        self._order_detail_product_repository.delete_by_id(order_detail_product_id)

    def update_by_id(self, order_detail_product_id, order_detail_product):
        self._order_detail_product_repository.update_by_id(
            order_detail_product_id, order_detail_product
        )

    def get_by_order_detail_id(self, order_detail_id):
        return self._order_detail_product_repository.get_by_order_detail_id(
            order_detail_id
        )
