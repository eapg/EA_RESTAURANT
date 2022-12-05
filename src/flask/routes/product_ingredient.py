from flask import Blueprint, make_response, request
from src.api.controllers.product_ingredient_controller import (
    ProductIngredientController,
)
from src.constants.http import HttpStatus
from src.flask.schemas.product_ingredient_schema import ProductIngredientSchema


def setup_product_ingredient_routes(ioc):

    product_ingredient_blueprint = Blueprint("product_ingredient_routes", __name__)
    product_ingredient_controller = ioc.get(ProductIngredientController)
    product_ingredient_schema = ProductIngredientSchema()
    product_ingredient_schemas = ProductIngredientSchema(many=True)

    @product_ingredient_blueprint.route("/product_ingredients", methods=["POST"])
    def add():
        json_product_ingredient_data = request.get_json()
        product_ingredient = product_ingredient_schema.load(
            json_product_ingredient_data
        )
        product_ingredient_added = product_ingredient_controller.add(product_ingredient)
        add_response = make_response(
            product_ingredient_schema.dump(product_ingredient_added),
            HttpStatus.CREATED.value,
        )
        return add_response

    @product_ingredient_blueprint.route(
        "/product_ingredients/<product_ingredient_id>", methods=["GET"]
    )
    def get_by_id(product_ingredient_id):
        product_ingredient = product_ingredient_controller.get_by_id(
            product_ingredient_id
        )
        get_response = make_response(product_ingredient_schema.dump(product_ingredient))
        return get_response

    @product_ingredient_blueprint.route("/product_ingredients", methods=["GET"])
    def get_all():
        product_ingredients = product_ingredient_controller.get_all()
        get_all_response = make_response(
            product_ingredient_schemas.dump(product_ingredients)
        )
        return get_all_response

    @product_ingredient_blueprint.route(
        "/product_ingredients/<product_ingredient_id>", methods=["PUT"]
    )
    def update_product_ingredient_by_id(product_ingredient_id):
        json_product_ingredient_data = request.get_json()
        product_ingredient = product_ingredient_schema.load(
            json_product_ingredient_data
        )
        product_ingredient_controller.update_by_id(
            product_ingredient_id, product_ingredient
        )
        product_ingredient_updated = product_ingredient_controller.get_by_id(
            product_ingredient_id
        )
        update_response = make_response(
            product_ingredient_schema.dump(product_ingredient_updated)
        )
        return update_response

    @product_ingredient_blueprint.route(
        "/product_ingredients/<product_ingredient_id>", methods=["DELETE"]
    )
    def delete_product_ingredient_by_id(product_ingredient_id):
        json_product_ingredient_data = request.get_json()
        product_ingredient = product_ingredient_schema.load(
            json_product_ingredient_data
        )
        product_ingredient_controller.delete_by_id(
            product_ingredient_id, product_ingredient
        )
        delete_response = make_response("", HttpStatus.OK.value)
        return delete_response

    @product_ingredient_blueprint.route(
        "/product_ingredients/by_product_id/<product_id>", methods=["GET"]
    )
    def get_by_product_id(product_id):
        product_ingredients = product_ingredient_controller.get_by_product_id(
            product_id
        )
        get_by_product_id_response = make_response(
            product_ingredient_schemas.dump(product_ingredients)
        )
        return get_by_product_id_response

    return product_ingredient_blueprint
