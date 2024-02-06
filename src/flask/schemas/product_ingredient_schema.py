# schemas fro serializing entities
from marshmallow import Schema, fields, post_load

from src.flask.utils import api_util
from src.lib.entities.sqlalchemy_orm_mapping import ProductIngredient


class ProductIngredientSchema(Schema):

    id = fields.Int()
    product_id = fields.Int()
    ingredient_id = fields.Int()
    quantity = fields.Int()
    cooking_type = fields.Str()
    created_by = fields.Int()
    updated_by = fields.Int()

    # pylint: disable=R0201
    @post_load
    def create_sqlalchemy_product_ingredient_entity(self, data, **kwargs):
        product_ingredient_to_fetch = ProductIngredient()
        product_ingredient = api_util.fetch_class_from_data(
            product_ingredient_to_fetch, data
        )

        return product_ingredient
