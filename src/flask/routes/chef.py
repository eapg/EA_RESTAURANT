from flask import Blueprint, request, make_response
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
        add_response = make_response(chef_schema.dump(chef_added), 201)
        return add_response

    @chef_blueprint.route("/chefs/<chef_id>", methods=["GET"])
    def get_by_id(chef_id):
        chef = chef_controller.get_by_id(chef_id)
        get_response = make_response(chef_schema.dump(chef))
        return get_response

    @chef_blueprint.route("/chefs", methods=["GET"])
    def get_all():
        chefs = chef_controller.get_all()
        get_all_response = make_response(chef_schemas.dump(chefs))
        return get_all_response

    @chef_blueprint.route("/chefs/<chef_id>", methods=["PUT"])
    def update_chef_by_id(chef_id):
        json_chef_data = request.get_json()
        chef = chef_schema.load(json_chef_data)
        chef_controller.update_by_id(chef_id, chef)
        chef_updated = chef_controller.get_by_id(chef_id)
        update_response = make_response(chef_schema.dump(chef_updated))
        return update_response

    @chef_blueprint.route("/chefs/<chef_id>", methods=["DELETE"])
    def delete_chef_by_id(chef_id):
        json_chef_data = request.get_json()
        chef = chef_schema.load(json_chef_data)
        chef_controller.delete_by_id(chef_id, chef)
        delete_response = make_response("", 200)
        return delete_response

    @chef_blueprint.route("/chefs/available", methods=["GET"])
    def get_available_chefs():
        available_chefs = chef_controller.get_available_chefs()
        get_available_response = make_response(chef_schemas.dump(available_chefs))
        return get_available_response

    return chef_blueprint
