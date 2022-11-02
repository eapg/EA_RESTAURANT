from flask import Blueprint, request
from src.api.controllers.chef_controller import ChefController
from src.flask.schemas.chef_schema import ChefSchema


def setup_chef_routes(ioc):

    chef_blueprint = Blueprint("chef_routes", __name__)
    chef_controller = ioc.get(ChefController)
    chef_schema = ChefSchema()
    chef_schemas = ChefSchema(many=True)

    @chef_blueprint.route("/chefs", methods=["POST"])
    def add():
        json_chef_data = request.get_json()
        chef = chef_schema.load(json_chef_data)
        chef_added = chef_controller.add(chef)
        return chef_schema.dump(chef_added)

    @chef_blueprint.route("/chefs/<chef_id>", methods=["GET"])
    def get_by_id(chef_id):
        chef = chef_controller.get_by_id(chef_id)
        return chef_schema.dump(chef)

    @chef_blueprint.route("/chefs", methods=["GET"])
    def get_all():
        chefs = chef_controller.get_all()
        return chef_schemas.dump(chefs)

    @chef_blueprint.route("/chefs/<chef_id>", methods=["PUT"])
    def update_chef_by_id(chef_id):
        json_chef_data = request.get_json()
        chef = chef_schema.load(json_chef_data)
        chef_controller.update_by_id(chef_id, chef)
        chef_updated = chef_controller.get_by_id(chef_id)
        return chef_schema.dump(chef_updated)

    @chef_blueprint.route("/chefs/<chef_id>", methods=["DELETE"])
    def delete_chef_by_id(chef_id):
        json_chef_data = request.get_json()
        chef = chef_schema.load(json_chef_data)
        chef_controller.delete_by_id(chef_id, chef)
        return f"Chef {chef_id} Deleted"

    @chef_blueprint.route("/chefs/available", methods=["GET"])
    def get_available_chefs():
        available_chefs = chef_controller.get_available_chefs()
        return chef_schemas.dump(available_chefs)

    return chef_blueprint
