from datetime import datetime

from sqlalchemy import sql

from src.constants.audit import Status
from src.core import ioc
from src.lib.entities import sqlalchemy_orm_mapping
from src.lib.repositories import order_status_history_repository


class OrderStatusHistoryRepositoryImpl(
    order_status_history_repository.OrderStatusHistoryRepository
):
    def __init__(self):

        ioc_instance = ioc.get_ioc_instance()
        self.session = ioc_instance.get_instance("sqlalchemy_session")

    def add(self, order_status_history):
        with self.session.begin():
            order_status_history.created_date = datetime.now()
            order_status_history.updated_by = order_status_history.created_by
            order_status_history.updated_date = order_status_history.created_date
            self.session.add(order_status_history)

    def get_by_id(self, order_status_history_id):
        return (
            self.session.query(sqlalchemy_orm_mapping.OrderStatusHistory)
            .filter(
                sqlalchemy_orm_mapping.OrderStatusHistory.id == order_status_history_id
            )
            .filter(
                sqlalchemy_orm_mapping.OrderStatusHistory.entity_status
                == Status.ACTIVE.value
            )
            .first()
        )

    def get_all(self):
        order_status_histories = self.session.query(
            sqlalchemy_orm_mapping.OrderStatusHistory
        ).filter(
            sqlalchemy_orm_mapping.OrderStatusHistory.entity_status
            == Status.ACTIVE.value
        )
        return list(order_status_histories)

    def delete_by_id(self, order_status_history_id, order_status_history):
        with self.session.begin():
            self.session.query(sqlalchemy_orm_mapping.OrderStatusHistory).filter(
                sqlalchemy_orm_mapping.OrderStatusHistory.id == order_status_history_id
            ).update(
                {
                    sqlalchemy_orm_mapping.OrderStatusHistory.entity_status: Status.DELETED.value,
                    sqlalchemy_orm_mapping.OrderStatusHistory.updated_date: datetime.now(),
                    sqlalchemy_orm_mapping.OrderStatusHistory.updated_by: order_status_history.updated_by,
                }
            )

    def update_by_id(self, order_status_history_id, order_status_history):
        with self.session.begin():
            order_status_history_to_be_updated = (
                self.session.query(sqlalchemy_orm_mapping.OrderStatusHistory)
                .filter(
                    sqlalchemy_orm_mapping.OrderStatusHistory.id
                    == order_status_history_id
                )
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
            self.session.query(sqlalchemy_orm_mapping.OrderStatusHistory)
            .filter(
                sqlalchemy_orm_mapping.OrderStatusHistory.entity_status
                == Status.ACTIVE.value
            )
            .filter(sqlalchemy_orm_mapping.OrderStatusHistory.order_id == order_id)
        )
        return list(order_status_histories)

    def get_last_status_history_by_order_id(self, order_id):
        last_status_history_by_order_id = (
            self.session.query(
                sql.func.max(sqlalchemy_orm_mapping.OrderStatusHistory.from_time)
            )
            .filter(sqlalchemy_orm_mapping.OrderStatusHistory.order_id == order_id)
            .first()
        )

        return last_status_history_by_order_id

    def set_next_status_history_by_order_id(self, order_id, new_status):
        with self.session.begin():
            last_order_status_history_from_time = self.session.query(
                sql.func.max(sqlalchemy_orm_mapping.OrderStatusHistory.from_time)
            ).first()

            last_order_status_history = (
                self.session.query(sqlalchemy_orm_mapping.OrderStatusHistory)
                .filter(
                    sqlalchemy_orm_mapping.OrderStatusHistory.entity_status
                    == Status.ACTIVE.value
                )
                .filter(sqlalchemy_orm_mapping.OrderStatusHistory.order_id == order_id)
                .filter(
                    sqlalchemy_orm_mapping.OrderStatusHistory.from_time
                    == last_order_status_history_from_time[0]
                )
                .first()
            )

            if last_order_status_history:
                last_order_status_history.to_status = new_status
                last_order_status_history.to_time = datetime.now()
                self.update_by_id(
                    last_order_status_history.id, last_order_status_history
                )

            new_status_history = sqlalchemy_orm_mapping.OrderStatusHistory()
            new_status_history.from_status = new_status
            new_status_history.from_time = datetime.now()
            new_status_history.entity_status = Status.ACTIVE.value
            new_status_history.order_id = order_id
            new_status_history.created_by = 2
            self.session.add(new_status_history)
