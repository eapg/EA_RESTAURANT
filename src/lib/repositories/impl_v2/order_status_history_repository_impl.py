from datetime import datetime

from injector import inject
from sqlalchemy import desc, select, text
from sqlalchemy.engine.base import Engine

from src.constants.audit import Status
from src.core.sqlalchemy_config import create_session
from src.lib.entities.sqlalchemy_orm_mapping import OrderStatusHistory
from src.lib.repositories.order_status_history_repository import (
    OrderStatusHistoryRepository,
)

SQL_QUERY_TO_UPDATE_ETL_STATUS = """
          UPDATE order_status_histories
             SET etl_status = 'PROCESSED'
           WHERE  id in :order_status_history_ids 
"""

SQL_QUERY_LATEST_ORDER_STATUS_HISTORIES_BY_ORDER_IDS = """
        WITH latest_order_status_histories_cte AS (
          SELECT osh.order_id, max(osh.from_time) AS max_from_time
            FROM order_status_histories osh
           WHERE osh.order_id IN :order_ids AND osh.entity_status = 'ACTIVE'
           GROUP BY osh.order_id
        )
            SELECT osh.*
              FROM order_status_histories AS osh
        INNER JOIN latest_order_status_histories_cte loshcte
                ON loshcte.order_id = osh.order_id AND loshcte.max_from_time = osh.from_time
"""


class OrderStatusHistoryRepositoryImpl(OrderStatusHistoryRepository):
    @inject
    def __init__(self, engine: Engine):

        self.engine = engine

    def add(self, order_status_history):
        session = create_session(self.engine)
        with session.begin():
            order_status_history.entity_status = Status.ACTIVE.value
            order_status_history.created_date = datetime.now()
            order_status_history.updated_by = order_status_history.created_by
            order_status_history.updated_date = order_status_history.created_date
            session.add(order_status_history)
            session.flush()
            session.refresh(order_status_history)
            return order_status_history

    def get_by_id(self, order_status_history_id):
        session = create_session(self.engine)
        return (
            session.query(OrderStatusHistory)
            .filter(OrderStatusHistory.entity_status == Status.ACTIVE.value)
            .filter(OrderStatusHistory.id == order_status_history_id)
            .first()
        )

    def get_all(self):
        session = create_session(self.engine)
        order_status_histories = session.query(OrderStatusHistory).filter(
            OrderStatusHistory.entity_status == Status.ACTIVE.value
        )
        return list(order_status_histories)

    def delete_by_id(self, order_status_history_id, order_status_history):
        session = create_session(self.engine)
        with session.begin():
            session.query(OrderStatusHistory).filter(
                OrderStatusHistory.id == order_status_history_id
            ).update(
                {
                    OrderStatusHistory.entity_status: Status.DELETED.value,
                    OrderStatusHistory.updated_date: datetime.now(),
                    OrderStatusHistory.updated_by: order_status_history.updated_by,
                }
            )

    def update_by_id(self, order_status_history_id, order_status_history):
        session = create_session(self.engine)
        with session.begin():
            order_status_history_to_be_updated = (
                session.query(OrderStatusHistory)
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
            session.add(order_status_history_to_be_updated)

    def get_by_order_id(self, order_id):
        session = create_session(self.engine)
        order_status_histories = (
            session.query(OrderStatusHistory)
            .filter(OrderStatusHistory.entity_status == Status.ACTIVE.value)
            .filter(OrderStatusHistory.order_id == order_id)
        )
        return list(order_status_histories)

    def get_last_order_status_histories_by_order_ids(self, order_ids):
        session = create_session(self.engine)
        order_status_histories = []

        with session.begin():
            sql_text = text(
                SQL_QUERY_LATEST_ORDER_STATUS_HISTORIES_BY_ORDER_IDS
            ).bindparams(order_ids=tuple(order_ids))
            order_status_histories.extend(
                session.scalars(
                    select(OrderStatusHistory).from_statement(sql_text)
                ).all()
            )

        return order_status_histories

    def set_next_status_history_by_order_id(self, order_id, new_status):
        session = create_session(self.engine)
        with session.begin():
            last_order_status_history = (
                session.query(OrderStatusHistory)
                .filter(OrderStatusHistory.order_id == order_id)
                .order_by(desc(OrderStatusHistory.from_time))
                .limit(1)
                .all()
            )

            if last_order_status_history:
                last_order_status_history[0].to_status = new_status
                last_order_status_history[0].to_time = datetime.now()
                session.add(last_order_status_history[0])

            new_status_history = OrderStatusHistory()
            new_status_history.from_status = new_status
            new_status_history.from_time = datetime.now()
            new_status_history.entity_status = Status.ACTIVE.value
            new_status_history.order_id = order_id
            new_status_history.created_by = 2
            new_status_history.updated_by = new_status_history.created_by
            session.add(new_status_history)

    def update_batch_processed(self, order_status_history_ids):

        with self.engine.begin() as conn:

            conn.execute(
                text(SQL_QUERY_TO_UPDATE_ETL_STATUS).bindparams(
                    order_status_history_ids=tuple(order_status_history_ids)
                )
            )

    def insert_new_or_updated_batch_order_status_histories(
        self, order_status_histories
    ):
        session = create_session(self.engine)
        with session.begin():
            session.bulk_save_objects(order_status_histories)

    def get_last_status_history_by_order_id(self, order_id):
        pass

    def get_unprocessed_order_status_histories(self):
        pass

    def get_order_status_histories_by_service(self, service, limit):
        pass
