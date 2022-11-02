# schemas fro serializing entities
from marshmallow import Schema, fields, post_load

from src.flask.utils import api_util
from src.lib.entities.sqlalchemy_orm_mapping import Chef


class ChefSchema(Schema):

    id = fields.Int()
    user_id = fields.Int()
    skill = fields.Int()
    created_by = fields.Int()
    updated_by = fields.Int()

    # pylint: disable=R0201
    @post_load
    def create_sqlalchemy_chef_entity(self, data, **kwargs):
        chef_to_fetch = Chef()
        chef = api_util.fetch_class_from_data(chef_to_fetch, data)

        return chef
