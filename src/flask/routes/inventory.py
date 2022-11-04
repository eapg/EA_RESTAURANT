from flask import Blueprint, make_response, request
from src.api.controllers.inventory_controller import InventoryController
from src.constants.http_status_code import HttpStatus
from src.flask.schemas.inventory_schema import InventorySchema


def setup_inventory_routes(ioc):

    inventory_blueprint = Blueprint("inventory_routes", __name__)
    inventory_controller = ioc.get(InventoryController)
    inventory_schema = InventorySchema()
    inventory_schemas = InventorySchema(many=True)

    @inventory_blueprint.route("/inventories", methods=["POST"])
    def add():
        json_inventory_data = request.get_json()
        inventory = inventory_schema.load(json_inventory_data)
        inventory_added = inventory_controller.add(inventory)
        add_response = make_response(
            inventory_schema.dump(inventory_added), HttpStatus.CREATED.value
        )
        return add_response

    @inventory_blueprint.route("/inventories/<inventory_id>", methods=["GET"])
    def get_by_id(inventory_id):
        inventory = inventory_controller.get_by_id(inventory_id)
        get_response = make_response(inventory_schema.dump(inventory))
        return get_response

    @inventory_blueprint.route("/inventories", methods=["GET"])
    def get_all():
        inventories = inventory_controller.get_all()
        get_all_response = make_response(inventory_schemas.dump(inventories))
        return get_all_response

    @inventory_blueprint.route("/inventories/<inventory_id>", methods=["PUT"])
    def update_inventory_by_id(inventory_id):
        json_inventory_data = request.get_json()
        inventory = inventory_schema.load(json_inventory_data)
        inventory_controller.update_by_id(inventory_id, inventory)
        inventory_updated = inventory_controller.get_by_id(inventory_id)
        update_response = make_response(inventory_schema.dump(inventory_updated))
        return update_response

    @inventory_blueprint.route("/inventories/<inventory_id>", methods=["DELETE"])
    def delete_inventory_by_id(inventory_id):
        json_inventory_data = request.get_json()
        inventory = inventory_schema.load(json_inventory_data)
        inventory_controller.delete_by_id(inventory_id, inventory)
        delete_response = make_response("", HttpStatus.OK.value)
        return delete_response

    return inventory_blueprint
