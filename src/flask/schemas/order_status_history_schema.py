# schemas fro serializing entities
from marshmallow import Schema, fields, post_load

from src.flask.utils import api_util
from src.lib.entities.sqlalchemy_orm_mapping import OrderStatusHistory


class OrderStatusHistorySchema(Schema):

    id = fields.Int()
    mongo_order_status_history_uuid = fields.Str()
    order_id = fields.Int()
    from_time = fields.DateTime()
    to_time = fields.DateTime()
    from_status = fields.Str()
    to_status = fields.Str()
    etl_status = fields.Str()
    created_by = fields.Int()
    updated_by = fields.Int()

    # pylint: disable=R0201
    @post_load
    def create_sqlalchemy_order_status_history_entity(self, data, **kwargs):
        order_status_history_to_fetch = OrderStatusHistory()
        order_status_history = api_util.fetch_class_from_data(
            order_status_history_to_fetch, data
        )

        return order_status_history
