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

    def delete_by_id(self, order_status_history_id, order_status_history):
        self._order_status_history_repository.delete_by_id(
            order_status_history_id, order_status_history
        )

    def update_by_id(self, order_status_history_id, order_status_history):
        self._order_status_history_repository.update_by_id(
            order_status_history_id, order_status_history
        )

    def get_by_order_id(self, order_id):
        return self._order_status_history_repository.get_by_order_id(order_id)

    def get_last_status_history_by_order_id(self, order_id):
        return (
            self._order_status_history_repository.get_last_status_history_by_order_id(
                order_id
            )
        )

    def set_next_status_history_by_order_id(self, order_id, new_status):
        self._order_status_history_repository.set_next_status_history_by_order_id(
            order_id, new_status
        )

    def update_batch_to_processed(self, order_status_history_ids):
        self.update_batch_to_processed(order_status_history_ids)

    def last_order_status_histories_by_order_ids(self, order_ids):
        return self._order_status_history_repository.get_last_order_status_histories_by_order_ids(
            self, order_ids
        )

    def insert_new_or_updated_batch_order_status_histories(
        self, order_status_histories
    ):
        self._order_status_history_repository.insert_new_or_updated_batch_order_status_histories(
            order_status_histories
        )
