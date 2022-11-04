from flask import Blueprint, make_response, request
from src.api.controllers.order_controller import OrderController
from src.constants.http_status_code import HttpStatus
from src.flask.schemas.order_schema import OrderSchema
from src.flask.schemas.product_ingredient_schema import ProductIngredientSchema


def setup_order_routes(ioc):

    order_blueprint = Blueprint("order_routes", __name__)
    order_controller = ioc.get(OrderController)
    order_schema = OrderSchema()
    order_schemas = OrderSchema(many=True)
    product_ingredient_schemas = ProductIngredientSchema(many=True)

    @order_blueprint.route("/orders", methods=["POST"])
    def add():
        json_order_data = request.get_json()
        order = order_schema.load(json_order_data)
        order_added = order_controller.add(order)
        add_response = make_response(
            order_schema.dump(order_added), HttpStatus.CREATED.value
        )
        return add_response

    @order_blueprint.route("/orders/<order_id>", methods=["GET"])
    def get_by_id(order_id):
        order = order_controller.get_by_id(order_id)
        get_response = make_response(order_schema.dump(order))
        return get_response

    @order_blueprint.route("/orders", methods=["GET"])
    def get_all():
        orders = order_controller.get_all()
        get_all_response = make_response(order_schemas.dump(orders))
        return get_all_response

    @order_blueprint.route("/orders/<order_id>", methods=["PUT"])
    def update_order_by_id(order_id):
        json_order_data = request.get_json()
        order = order_schema.load(json_order_data)
        order_controller.update_by_id(order_id, order)
        order_updated = order_controller.get_by_id(order_id)
        update_response = make_response(order_schema.dump(order_updated))
        return update_response

    @order_blueprint.route("/orders/<order_id>", methods=["DELETE"])
    def delete_order_by_id(order_id):
        json_order_data = request.get_json()
        order = order_schema.load(json_order_data)
        order_controller.delete_by_id(order_id, order)
        delete_response = make_response("", HttpStatus.OK.value)
        return delete_response

    @order_blueprint.route("/orders/by_order_status/<order_status>", methods=["GET"])
    def get_orders_by_status(order_status):
        args = request.args
        order_limit = args["limit"]
        orders_by_status = order_controller.get_orders_by_status(
            order_status=order_status, order_limit=order_limit
        )
        get_by_status_response = make_response(order_schemas.dump(orders_by_status))
        return get_by_status_response

    @order_blueprint.route("/orders/<order_id>/ingredients", methods=["GET"])
    def get_order_ingredients_by_order_id(order_id):
        order_ingredients = order_controller.get_order_ingredients_by_order_id(order_id)
        get_order_ingredients_response = make_response(
            product_ingredient_schemas.dump(order_ingredients)
        )
        return get_order_ingredients_response

    return order_blueprint
