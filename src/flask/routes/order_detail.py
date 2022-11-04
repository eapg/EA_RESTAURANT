from flask import Blueprint, make_response, request
from src.api.controllers.order_detail_controller import (
    OrderDetailController,
)
from src.constants.http_status_code import HttpStatus
from src.flask.schemas.order_detail_schema import OrderDetailSchema


def setup_order_detail_routes(ioc):

    order_detail_blueprint = Blueprint("order_detail_routes", __name__)
    order_detail_controller = ioc.get(OrderDetailController)
    order_detail_schema = OrderDetailSchema()
    order_detail_schemas = OrderDetailSchema(many=True)

    @order_detail_blueprint.route("/order_details", methods=["POST"])
    def add():
        json_order_detail_data = request.get_json()
        order_detail = order_detail_schema.load(
            json_order_detail_data
        )
        order_detail_added = order_detail_controller.add(
            order_detail
        )
        add_response = make_response(
            order_detail_schema.dump(order_detail_added),
            HttpStatus.CREATED.value,
        )
        return add_response

    @order_detail_blueprint.route(
        "/order_details/<order_detail_id>", methods=["GET"]
    )
    def get_by_id(order_detail_id):
        order_detail = order_detail_controller.get_by_id(
            order_detail_id
        )
        get_response = make_response(
            order_detail_schema.dump(order_detail)
        )
        return get_response

    @order_detail_blueprint.route("/order_details", methods=["GET"])
    def get_all():
        order_details = order_detail_controller.get_all()
        get_all_response = make_response(
            order_detail_schemas.dump(order_details)
        )
        return get_all_response

    @order_detail_blueprint.route(
        "/order_details/<order_detail_id>", methods=["PUT"]
    )
    def update_order_detail_by_id(order_detail_id):
        json_order_detail_data = request.get_json()
        order_detail = order_detail_schema.load(
            json_order_detail_data
        )
        order_detail_controller.update_by_id(
            order_detail_id, order_detail
        )
        order_detail_updated = order_detail_controller.get_by_id(
            order_detail_id
        )
        update_response = make_response(
            order_detail_schema.dump(order_detail_updated)
        )
        return update_response

    @order_detail_blueprint.route(
        "/order_details/<order_detail_id>", methods=["DELETE"]
    )
    def delete_order_detail_by_id(order_detail_id):
        json_order_detail_data = request.get_json()
        order_detail = order_detail_schema.load(
            json_order_detail_data
        )
        order_detail_controller.delete_by_id(
            order_detail_id, order_detail
        )
        delete_response = make_response("", HttpStatus.OK.value)
        return delete_response

    @order_detail_blueprint.route(
        "/order_details/by_order_id/<order_id>", methods=["GET"]
    )
    def get_by_order_id(order_id):
        order_details = order_detail_controller.get_by_order_id(
            order_id
        )
        get_by_ingredient_id_response = make_response(
            order_detail_schemas.dump(order_details)
        )
        return get_by_ingredient_id_response

    return order_detail_blueprint
