# schemas fro serializing entities
from marshmallow import Schema, fields, post_load

from src.flask.utils import api_util
from src.lib.entities.sqlalchemy_orm_mapping import OrderDetail


class OrderDetailSchema(Schema):

    id = fields.Int()
    order_id = fields.Int()
    product_id = fields.Int()
    quantity = fields.Int()
    created_by = fields.Int()
    updated_by = fields.Int()

    # pylint: disable=R0201
    @post_load
    def create_sqlalchemy_order_detail_entity(self, data, **kwargs):
        order_detail_to_fetch = OrderDetail()
        order_detail = api_util.fetch_class_from_data(order_detail_to_fetch, data)

        return order_detail
