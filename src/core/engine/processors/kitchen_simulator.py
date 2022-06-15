from abc import ABCMeta

from src.core.engine.processors.abstract_processor import AbstractProcessor
from src.core.ioc import get_ioc_instance
from src.core.order_manager import OrderManager
from src.constants.order_status import OrderStatus
from src.utils.order_util import compute_order_estimated_time


class KitchenSimulator(AbstractProcessor, metaclass=ABCMeta):
    def __init__(self, app_processor_config, app_context=None):
        super().__init__(
            app_processor_config=app_processor_config, app_context=app_context
        )

        ioc = get_ioc_instance()
        self.order_controller = ioc.get_instance("order_controller")
        self.order_status_history_controller = ioc.get_instance(
            "order_status_history_controller"
        )
        self.chef_controller = ioc.get_instance("chef_controller")
        self.order_manager = OrderManager()

    def process(self, delta_time):
        print("Waiting orders")
        self.assign_orders_to_available_chefs()

    def assign_orders_to_available_chefs(self):

        orders_to_process = self.order_controller.get_orders_to_process(
            order_limit=1000
        )
        orders_validation_map = self.order_controller.get_validated_orders_map(
            orders_to_process
        )
        available_chef_ids = self.chef_controller.get_available_chefs()

        if available_chef_ids:

            order_in_turn_id = self.order_manager.get_queue_from_status(
                OrderStatus.NEW_ORDER
            )
            order_to_be_assigned = list(
                filter((lambda order: order.id == order_in_turn_id), orders_to_process)
            )

            if orders_validation_map[order_to_be_assigned[0].id]:
                self._assign_to_chef_and_send_to_in_process(
                    order_to_be_assigned[0], available_chef_ids[0]
                )

            else:
                self._order_send_to_cancel(order_to_be_assigned[0])

    def _assign_to_chef_and_send_to_in_process(
        self, order_to_be_assign, available_chef
    ):
        order_to_be_assign.assigned_chef_id = available_chef
        order_to_be_assign.status = OrderStatus.IN_PROCESS
        order_to_be_assign.estimated_time = compute_order_estimated_time(
            self.order_controller.get_order_ingredients_by_order_id, available_chef
        )
        self.order_controller.update_by_id(order_to_be_assign.id, order_to_be_assign)
        self.order_status_history_controller.set_next_status_history_by_order_id(
            order_to_be_assign.id, order_to_be_assign.status
        )
        self.order_manager.add_to_queue(order_to_be_assign)

    def _order_send_to_cancel(self, order_to_be_cancel):
        order_to_be_cancel.status = OrderStatus.CANCELLED
        self.order_controller.update_by_id(order_to_be_cancel.id, order_to_be_cancel)
        self.order_status_history_controller.set_next_status_history_by_order_id(
            order_to_be_cancel.id, order_to_be_cancel.status
        )
        self.order_manager.add_to_queue(order_to_be_cancel)
