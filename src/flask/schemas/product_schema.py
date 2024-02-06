# schemas fro serializing entities
from marshmallow import Schema, fields, post_load

from src.flask.utils import api_util
from src.lib.entities.sqlalchemy_orm_mapping import Product


class ProductSchema(Schema):

    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    created_by = fields.Int()
    updated_by = fields.Int()

    # pylint: disable=R0201
    @post_load
    def create_sqlalchemy_product_entity(self, data, **kwargs):
        product_to_fetch = Product()
        product = api_util.fetch_class_from_data(product_to_fetch, data)

        return product
