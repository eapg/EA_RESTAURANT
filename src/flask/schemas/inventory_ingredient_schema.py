# schemas fro serializing entities
from marshmallow import Schema, fields, post_load

from src.flask.utils import api_util
from src.lib.entities.sqlalchemy_orm_mapping import InventoryIngredient


class InventoryIngredientSchema(Schema):

    id = fields.Int()
    ingredient_id = fields.Int()
    inventory_id = fields.Int()
    quantity = fields.Int()
    created_by = fields.Int()
    updated_by = fields.Int()

    # pylint: disable=R0201
    @post_load
    def create_sqlalchemy_inventory_ingredient_entity(self, data, **kwargs):
        inventory_ingredient_to_fetch = InventoryIngredient()
        inventory_ingredient = api_util.fetch_class_from_data(
            inventory_ingredient_to_fetch, data
        )

        return inventory_ingredient
