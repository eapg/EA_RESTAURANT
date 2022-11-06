from flask import Blueprint, make_response, request
from src.api.controllers.order_status_history_controller import (
    OrderStatusHistoryController,
)
from src.constants.http_status_code import HttpStatus
from src.flask.schemas.order_status_history_schema import OrderStatusHistorySchema


def setup_order_status_history_routes(ioc):

    order_status_history_blueprint = Blueprint("order_status_history_routes", __name__)
    order_status_history_controller = ioc.get(OrderStatusHistoryController)
    order_status_history_schema = OrderStatusHistorySchema()
    order_status_history_schemas = OrderStatusHistorySchema(many=True)

    @order_status_history_blueprint.route("/order_status_histories", methods=["POST"])
    def add():
        json_order_status_history_data = request.get_json()
        order_status_history = order_status_history_schema.load(
            json_order_status_history_data
        )
        order_status_history_added = order_status_history_controller.add(
            order_status_history
        )
        add_response = make_response(
            order_status_history_schema.dump(order_status_history_added),
            HttpStatus.CREATED.value,
        )
        return add_response

    @order_status_history_blueprint.route(
        "/order_status_histories/<order_status_history_id>", methods=["GET"]
    )
    def get_by_id(order_status_history_id):
        order_status_history = order_status_history_controller.get_by_id(
            order_status_history_id
        )
        get_response = make_response(
            order_status_history_schema.dump(order_status_history)
        )
        return get_response

    @order_status_history_blueprint.route("/order_status_histories", methods=["GET"])
    def get_all():
        order_status_histories = order_status_history_controller.get_all()
        get_all_response = make_response(
            order_status_history_schemas.dump(order_status_histories)
        )
        return get_all_response

    @order_status_history_blueprint.route(
        "/order_status_histories/<order_status_history_id>", methods=["PUT"]
    )
    def update_order_status_history_by_id(order_status_history_id):
        json_order_status_history_data = request.get_json()
        order_status_history = order_status_history_schema.load(
            json_order_status_history_data
        )
        order_status_history_controller.update_by_id(
            order_status_history_id, order_status_history
        )
        order_status_history_updated = order_status_history_controller.get_by_id(
            order_status_history_id
        )
        update_response = make_response(
            order_status_history_schema.dump(order_status_history_updated)
        )
        return update_response

    @order_status_history_blueprint.route(
        "/order_status_histories/<order_status_history_id>", methods=["DELETE"]
    )
    def delete_order_status_history_by_id(order_status_history_id):
        json_order_status_history_data = request.get_json()
        order_status_history = order_status_history_schema.load(
            json_order_status_history_data
        )
        order_status_history_controller.delete_by_id(
            order_status_history_id, order_status_history
        )
        delete_response = make_response("", HttpStatus.OK.value)
        return delete_response

    @order_status_history_blueprint.route(
        "/order_status_histories/by_order_id/<order_id>", methods=["GET"]
    )
    def get_by_order_id(order_id):
        order_status_histories_by_order_id = (
            order_status_history_controller.get_by_order_id(order_id)
        )
        get_by_order_id_response = make_response(
            order_status_history_schemas.dump(order_status_histories_by_order_id)
        )
        return get_by_order_id_response

    return order_status_history_blueprint
