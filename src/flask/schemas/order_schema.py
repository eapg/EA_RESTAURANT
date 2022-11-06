# schemas fro serializing entities
from marshmallow import Schema, fields, post_load

from src.flask.utils import api_util
from src.lib.entities.sqlalchemy_orm_mapping import Order


class OrderSchema(Schema):

    id = fields.Int()
    status = fields.Str()
    assigned_chef_id = fields.Int()
    client_id = fields.Int()
    created_by = fields.Int()
    updated_by = fields.Int()

    # pylint: disable=R0201
    @post_load
    def create_sqlalchemy_order_entity(self, data, **kwargs):
        order_to_fetch = Order()
        order = api_util.fetch_class_from_data(order_to_fetch, data)

        return order
