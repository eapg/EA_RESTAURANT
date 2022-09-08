from datetime import datetime

from sqlalchemy import desc

from src.constants.audit import Status
from sqlalchemy.sql import func
from src.lib.entities.sqlalchemy_orm_mapping import OrderStatusHistory
from src.lib.repositories.order_status_history_repository import (
    OrderStatusHistoryRepository,
)


class OrderStatusHistoryRepositoryImpl(OrderStatusHistoryRepository):
    def __init__(self, session):

        self.session = session

    def add(self, order_status_history):
        with self.session.begin():
            order_status_history.created_date = datetime.now()
            order_status_history.updated_by = order_status_history.created_by
            order_status_history.updated_date = order_status_history.created_date
            self.session.add(order_status_history)

    def get_by_id(self, order_status_history_id):
        return (
            self.session.query(OrderStatusHistory)
            .filter(OrderStatusHistory.id == order_status_history_id)
            .filter(OrderStatusHistory.entity_status == Status.ACTIVE.value)
            .first()
        )

    def get_all(self):
        order_status_histories = self.session.query(OrderStatusHistory).filter(
            OrderStatusHistory.entity_status == Status.ACTIVE.value
        )
        return list(order_status_histories)

    def delete_by_id(self, order_status_history_id, order_status_history):
        with self.session.begin():
            self.session.query(OrderStatusHistory).filter(
                OrderStatusHistory.id == order_status_history_id
            ).update(
                {
                    OrderStatusHistory.entity_status: Status.DELETED.value,
                    OrderStatusHistory.updated_date: datetime.now(),
                    OrderStatusHistory.updated_by: order_status_history.updated_by,
                }
            )

    def update_by_id(self, order_status_history_id, order_status_history):
        with self.session.begin():
            order_status_history_to_be_updated = (
                self.session.query(OrderStatusHistory)
                .filter(OrderStatusHistory.id == order_status_history_id)
                .first()
            )
            order_status_history_to_be_updated.order_id = (
                order_status_history.order_id
                or order_status_history_to_be_updated.order_id
            )
            order_status_history_to_be_updated.from_time = (
                order_status_history.from_time
                or order_status_history_to_be_updated.from_time
            )
            order_status_history_to_be_updated.to_time = (
                order_status_history.to_time
                or order_status_history_to_be_updated.to_time
            )
            order_status_history_to_be_updated.from_status = (
                order_status_history.from_status
                or order_status_history_to_be_updated.from_status
            )
            order_status_history_to_be_updated.to_status = (
                order_status_history.to_status
                or order_status_history_to_be_updated.to_status
            )
            order_status_history_to_be_updated.updated_date = datetime.now()
            order_status_history_to_be_updated.updated_by = (
                order_status_history.updated_by
            )
            self.session.add(order_status_history_to_be_updated)

    def get_by_order_id(self, order_id):
        order_status_histories = (
            self.session.query(OrderStatusHistory)
            .filter(OrderStatusHistory.entity_status == Status.ACTIVE.value)
            .filter(OrderStatusHistory.order_id == order_id)
        )
        return list(order_status_histories)

    def get_last_status_history_by_order_id(self, order_id):
        last_status_history_by_order_id = (
            self.session.query(OrderStatusHistory)
                .filter(OrderStatusHistory.order_id == order_id)
                .order_by(desc(OrderStatusHistory.from_time))
                .limit(1)
                .all()
        )

        return last_status_history_by_order_id[0]

    def set_next_status_history_by_order_id(self, order_id, new_status):
        with self.session.begin():
            last_order_status_history = (
                self.session.query(OrderStatusHistory)
                    .filter(OrderStatusHistory.order_id == order_id)
                    .order_by(desc(OrderStatusHistory.from_time))
                    .limit(1)
                    .all()
            )

            if last_order_status_history:
                last_order_status_history[0].to_status = new_status
                last_order_status_history[0].to_time = datetime.now()
                self.session.add(last_order_status_history[0])

            new_status_history = OrderStatusHistory()
            new_status_history.from_status = new_status
            new_status_history.from_time = datetime.now()
            new_status_history.entity_status = Status.ACTIVE.value
            new_status_history.order_id = order_id
            new_status_history.created_by = 2
            new_status_history.updated_by = new_status_history.created_by
            self.session.add(new_status_history)

