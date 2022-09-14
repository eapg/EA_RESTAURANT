"""mongo-initial-data

Revision ID: da1fd865c698
Revises: e96d49093b33
Create Date: 2022-09-14 09:54:00.367087

"""
from alembic import op
from sqlalchemy.orm.session import Session
from src.constants.audit import Status
from src.core.mongo_engine_config import mongo_engine_connexion

# revision identifiers, used by Alembic.
from src.lib.entities import sqlalchemy_orm_mapping
from src.lib.entities import mongo_engine_odm_mapping

revision = "da1fd865c698"
down_revision = "e96d49093b33"
branch_labels = None
depends_on = None


def upgrade() -> None:
    mongo_engine_connexion()

    session = Session(bind=op.get_bind())

    order_status_histories = session.query(
        sqlalchemy_orm_mapping.OrderStatusHistory
    ).filter(
        sqlalchemy_orm_mapping.OrderStatusHistory.entity_status == Status.ACTIVE.value
    )
    for order_status_history in list(order_status_histories):
        mongo_order_status_history = mongo_engine_odm_mapping.OrderStatusHistory()
        mongo_order_status_history._id = order_status_history.id
        mongo_order_status_history.order_id = order_status_history.id
        mongo_order_status_history.from_status = order_status_history.from_status
        mongo_order_status_history.to_status = order_status_history.to_status
        mongo_order_status_history.from_time = order_status_history.from_time
        mongo_order_status_history.to_time = order_status_history.to_time
        mongo_order_status_history.entity_status = order_status_history.entity_status
        mongo_order_status_history.created_by = order_status_history.created_by
        mongo_order_status_history.created_date = order_status_history.created_date
        mongo_order_status_history.updated_by = order_status_history.updated_by
        mongo_order_status_history.updated_date = order_status_history.updated_date
        mongo_order_status_history.save()


def downgrade() -> None:
    pass
