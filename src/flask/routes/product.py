from flask import Blueprint, make_response, request
from src.api.controllers.product_controller import ProductController
from src.constants.http import HttpStatus
from src.flask.schemas.product_schema import ProductSchema


def setup_product_routes(ioc):

    product_blueprint = Blueprint("product_routes", __name__)
    product_controller = ioc.get(ProductController)
    product_schema = ProductSchema()
    product_schemas = ProductSchema(many=True)

    @product_blueprint.route("/products", methods=["POST"])
    def add():
        json_product_data = request.get_json()
        product = product_schema.load(json_product_data)
        product_added = product_controller.add(product)
        add_response = make_response(
            product_schema.dump(product_added), HttpStatus.CREATED.value
        )
        return add_response

    @product_blueprint.route("/products/<product_id>", methods=["GET"])
    def get_by_id(product_id):
        product = product_controller.get_by_id(product_id)
        get_response = make_response(product_schema.dump(product))
        return get_response

    @product_blueprint.route("/products", methods=["GET"])
    def get_all():
        products = product_controller.get_all()
        get_all_response = make_response(product_schemas.dump(products))
        return get_all_response

    @product_blueprint.route("/products/<product_id>", methods=["PUT"])
    def update_product_by_id(product_id):
        json_product_data = request.get_json()
        product = product_schema.load(json_product_data)
        product_controller.update_by_id(product_id, product)
        product_updated = product_controller.get_by_id(product_id)
        update_response = make_response(product_schema.dump(product_updated))
        return update_response

    @product_blueprint.route("/products/<product_id>", methods=["DELETE"])
    def delete_product_by_id(product_id):
        json_product_data = request.get_json()
        product = product_schema.load(json_product_data)
        product_controller.delete_by_id(product_id, product)
        delete_response = make_response("", HttpStatus.OK.value)
        return delete_response

    return product_blueprint
