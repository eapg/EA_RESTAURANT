class OrderDetailController:
    def __init__(self, order_detail_repository):
        self._order_detail_repository = (
            order_detail_repository  # order_detailRepository
        )

    def add(self, order_detail):
        self._order_detail_repository.add(order_detail)

    def get_by_id(self, order_detail_id):
        return self._order_detail_repository.get_by_id(order_detail_id)

    def get_all(self):
        return self._order_detail_repository.get_all()

    def delete_by_id(self, order_detail_id, order_detail):
        self._order_detail_repository.delete_by_id(order_detail_id, order_detail)

    def update_by_id(self, order_detail_id, order_detail):
        self._order_detail_repository.update_by_id(order_detail_id, order_detail)

    def get_by_order_id(self, order_id):
        return self._order_detail_repository.get_by_order_id(order_id)
