class OrderController:
    def __init__(self, order_repository):
        self._order_repository = order_repository  # orderRepository

    def add(self, order):
        self._order_repository.add(order)

    def get_by_id(self, order_id):
        return self._order_repository.get_by_id(order_id)

    def get_all(self):
        return self._order_repository.get_all()

    def delete_by_id(self, order_id, order):
        self._order_repository.delete_by_id(order_id, order)

    def update_by_id(self, order_id, order):
        self._order_repository.update_by_id(order_id, order)

    def get_orders_by_status(self, order_status, order_limit=None):
        return self._order_repository.get_orders_by_status(order_status, order_limit)

    def get_order_ingredients_by_order_id(self, order_id):
        return self._order_repository.get_order_ingredients_by_order_id(order_id)

    def get_validated_orders_map(self, orders_to_process):
        return self._order_repository.get_validated_orders_map(orders_to_process)

    def reduce_order_ingredients_from_inventory(self, order_id):
        self._order_repository.reduce_order_ingredients_from_inventory(order_id)
