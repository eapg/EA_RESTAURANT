class OrderStatusHistoryController:
    def __init__(self, order_status_history_repository):
        self._order_status_history_repository = (
            order_status_history_repository  # order_status_historyRepository
        )

    def add(self, order_status_history):
        self._order_status_history_repository.add(order_status_history)

    def get_by_id(self, order_status_history_id):
        return self._order_status_history_repository.get_by_id(order_status_history_id)

    def get_all(self):
        return self._order_status_history_repository.get_all()

    def delete_by_id(self, order_status_history_id):
        self._order_status_history_repository.delete_by_id(order_status_history_id)

    def update_by_id(self, order_status_history_id, order_status_history):
        self._order_status_history_repository.update_by_id(
            order_status_history_id, order_status_history
        )

    def get_by_order_id(self, order_id):
        return self._order_status_history_repository.get_by_order_id(order_id)
