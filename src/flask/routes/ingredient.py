from flask import Blueprint, request, make_response
from src.api.controllers.ingredient_controller import IngredientController
from src.flask.schemas.ingredient_schema import IngredientSchema


def setup_ingredient_routes(ioc):

    ingredient_blueprint = Blueprint("ingredient_routes", __name__)
    ingredient_controller = ioc.get(IngredientController)
    ingredient_schema = IngredientSchema()
    ingredient_schemas = IngredientSchema(many=True)

    @ingredient_blueprint.route("/ingredients", methods=["POST"])
    def add():
        json_ingredient_data = request.get_json()
        ingredient = ingredient_schema.load(json_ingredient_data)
        ingredient_added = ingredient_controller.add(ingredient)
        add_response = make_response(ingredient_schema.dump(ingredient_added), 201)
        return add_response

    @ingredient_blueprint.route("/ingredients/<ingredient_id>", methods=["GET"])
    def get_by_id(ingredient_id):
        ingredient = ingredient_controller.get_by_id(ingredient_id)
        get_response = make_response(ingredient_schema.dump(ingredient))
        return get_response

    @ingredient_blueprint.route("/ingredients", methods=["GET"])
    def get_all():
        ingredients = ingredient_controller.get_all()
        get_all_response = make_response(ingredient_schemas.dump(ingredients))
        return get_all_response

    @ingredient_blueprint.route("/ingredients/<ingredient_id>", methods=["PUT"])
    def update_ingredient_by_id(ingredient_id):
        json_ingredient_data = request.get_json()
        ingredient = ingredient_schema.load(json_ingredient_data)
        ingredient_controller.update_by_id(ingredient_id, ingredient)
        ingredient_updated = ingredient_controller.get_by_id(ingredient_id)
        update_response = make_response(ingredient_schema.dump(ingredient_updated))
        return update_response

    @ingredient_blueprint.route("/ingredients/<ingredient_id>", methods=["DELETE"])
    def delete_ingredient_by_id(ingredient_id):
        json_ingredient_data = request.get_json()
        ingredient = ingredient_schema.load(json_ingredient_data)
        ingredient_controller.delete_by_id(ingredient_id, ingredient)
        delete_response = make_response("", 200)
        return delete_response

    return ingredient_blueprint
