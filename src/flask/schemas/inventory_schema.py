# schemas fro serializing entities
from marshmallow import Schema, fields, post_load

from src.flask.utils import api_util
from src.lib.entities.sqlalchemy_orm_mapping import Inventory


class InventorySchema(Schema):

    id = fields.Int()
    name = fields.Str()
    created_by = fields.Int()
    updated_by = fields.Int()

    # pylint: disable=R0201
    @post_load
    def create_sqlalchemy_inventory_entity(self, data, **kwargs):
        inventory_to_fetch = Inventory()
        inventory = api_util.fetch_class_from_data(inventory_to_fetch, data)

        return inventory
