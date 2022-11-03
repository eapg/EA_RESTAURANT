from flask import Blueprint, request, make_response
from src.api.controllers.inventory_ingredient_controller import (
    InventoryIngredientController,
)
from src.flask.schemas.inventory_ingredient_schema import InventoryIngredientSchema


def setup_inventory_ingredient_routes(ioc):

    inventory_ingredient_blueprint = Blueprint("inventory_ingredient_routes", __name__)
    inventory_ingredient_controller = ioc.get(InventoryIngredientController)
    inventory_ingredient_schema = InventoryIngredientSchema()
    inventory_ingredient_schemas = InventoryIngredientSchema(many=True)

    @inventory_ingredient_blueprint.route("/inventory_ingredients", methods=["POST"])
    def add():
        json_inventory_ingredient_data = request.get_json()
        inventory_ingredient = inventory_ingredient_schema.load(
            json_inventory_ingredient_data
        )
        inventory_ingredient_added = inventory_ingredient_controller.add(
            inventory_ingredient
        )
        add_response = make_response(
            inventory_ingredient_schema.dump(inventory_ingredient_added), 201
        )
        return add_response

    @inventory_ingredient_blueprint.route(
        "/inventory_ingredients/<inventory_ingredient_id>", methods=["GET"]
    )
    def get_by_id(inventory_ingredient_id):
        inventory_ingredient = inventory_ingredient_controller.get_by_id(
            inventory_ingredient_id
        )
        get_response = make_response(
            inventory_ingredient_schema.dump(inventory_ingredient)
        )
        return get_response

    @inventory_ingredient_blueprint.route("/inventory_ingredients", methods=["GET"])
    def get_all():
        inventory_ingredients = inventory_ingredient_controller.get_all()
        get_all_response = make_response(
            inventory_ingredient_schemas.dump(inventory_ingredients)
        )
        return get_all_response

    @inventory_ingredient_blueprint.route(
        "/inventory_ingredients/<inventory_ingredient_id>", methods=["PUT"]
    )
    def update_inventory_ingredient_by_id(inventory_ingredient_id):
        json_inventory_ingredient_data = request.get_json()
        inventory_ingredient = inventory_ingredient_schema.load(
            json_inventory_ingredient_data
        )
        inventory_ingredient_controller.update_by_id(
            inventory_ingredient_id, inventory_ingredient
        )
        inventory_ingredient_updated = inventory_ingredient_controller.get_by_id(
            inventory_ingredient_id
        )
        update_response = make_response(
            inventory_ingredient_schema.dump(inventory_ingredient_updated)
        )
        return update_response

    @inventory_ingredient_blueprint.route(
        "/inventory_ingredients/<inventory_ingredient_id>", methods=["DELETE"]
    )
    def delete_inventory_ingredient_by_id(inventory_ingredient_id):
        json_inventory_ingredient_data = request.get_json()
        inventory_ingredient = inventory_ingredient_schema.load(
            json_inventory_ingredient_data
        )
        inventory_ingredient_controller.delete_by_id(
            inventory_ingredient_id, inventory_ingredient
        )
        delete_response = make_response("", 200)
        return delete_response

    @inventory_ingredient_blueprint.route(
        "/inventory_ingredients/by_ingredient_id/<ingredient_id>", methods=["GET"]
    )
    def get_by_ingredient_id(ingredient_id):
        inventory_ingredients = inventory_ingredient_controller.get_by_ingredient_id(
            ingredient_id
        )
        get_by_ingredient_id_response = make_response(
            inventory_ingredient_schemas.dump(inventory_ingredients)
        )
        return get_by_ingredient_id_response

    return inventory_ingredient_blueprint
