from datetime import datetime

from src.constants.audit import Status
from src.lib.entities.sqlalchemy_orm_mapping import OrderDetail
from src.lib.repositories.order_detail_repository import OrderDetailRepository


class OrderDetailRepositoryImpl(OrderDetailRepository):
    def __init__(self, session):

        self.session = session

    def add(self, order_detail):
        with self.session.begin():
            order_detail.created_date = datetime.now()
            order_detail.updated_by = order_detail.created_by
            order_detail.updated_date = order_detail.created_date
            self.session.add(order_detail)

    def get_by_id(self, order_detail_id):
        return (
            self.session.query(OrderDetail)
            .filter(OrderDetail.id == order_detail_id)
            .filter(OrderDetail.entity_status == Status.ACTIVE.value)
            .first()
        )

    def get_all(self):
        order_details = self.session.query(OrderDetail).filter(
            OrderDetail.entity_status == Status.ACTIVE.value
        )
        return list(order_details)

    def delete_by_id(self, order_detail_id, order_detail):
        with self.session.begin():
            self.session.query(OrderDetail).filter(
                OrderDetail.id == order_detail_id
            ).update(
                {
                    OrderDetail.entity_status: Status.DELETED.value,
                    OrderDetail.updated_date: datetime.now(),
                    OrderDetail.updated_by: order_detail.updated_by,
                }
            )

    def update_by_id(self, order_detail_id, order_detail):
        with self.session.begin():
            order_detail_to_be_updated = (
                self.session.query(OrderDetail)
                .filter(OrderDetail.id == order_detail_id)
                .first()
            )
            order_detail_to_be_updated.user_id = (
                order_detail.user_id or order_detail_to_be_updated.user_id
            )
            order_detail_to_be_updated.skill = (
                order_detail.skill or order_detail_to_be_updated.skill
            )
            order_detail_to_be_updated.updated_date = datetime.now()
            order_detail_to_be_updated.updated_by = order_detail.updated_by
            self.session.add(order_detail_to_be_updated)

    def get_by_order_id(self, order_id):
        order_details = (
            self.session.query(OrderDetail)
            .filter(OrderDetail.entity_status == Status.ACTIVE.value)
            .filter(OrderDetail.order_id == order_id)
        )
        return list(order_details)