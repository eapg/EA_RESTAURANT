from abc import ABCMeta

from src.core.engine.processors.abstract_processor import AbstractProcessor
from src.core.ioc import get_ioc_instance
from src.core.order_manager import ORDER_QUEUE_STATUS_TO_CHUNK_LIMIT_MAP
from src.constants.order_status import OrderStatus
from src.utils.order_util import compute_order_estimated_time
from src.utils.time_util import get_unix_time_stamp_milliseconds
from datetime import datetime, timedelta


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
        self.order_manager = ioc.get_instance("order_manager")

    def process(self, delta_time):

        self.process_new_orders()
        self.process_orders_in_process()

    def process_new_orders(self):

        orders_to_process = self.order_controller.get_orders_by_status(
            OrderStatus.NEW_ORDER,
            order_limit=ORDER_QUEUE_STATUS_TO_CHUNK_LIMIT_MAP[OrderStatus.NEW_ORDER],
        )
        orders_validation_map = self.order_controller.get_validated_orders_map(
            orders_to_process
        )
        available_chef_ids = self.chef_controller.get_available_chefs()

        if available_chef_ids:

            order_in_turn_id = self.order_manager.get_queue_from_status(
                OrderStatus.NEW_ORDER
            )

            if order_in_turn_id:
                order_to_be_assigned = list(
                    filter(
                        (lambda order: order.id == order_in_turn_id), orders_to_process
                    )
                )

                if orders_validation_map[order_to_be_assigned[0].id]:
                    self._assign_to_chef_and_send_to_in_process(
                        order_to_be_assigned[0], available_chef_ids[0]
                    )

                else:
                    self._order_send_to_cancel(order_to_be_assigned[0])

    def process_orders_in_process(self):

        order_id_to_be_checked = self.order_manager.get_queue_from_status(
            OrderStatus.IN_PROCESS
        )

        if order_id_to_be_checked:
            order_to_be_checked = self.order_controller.get_by_id(
                order_id_to_be_checked
            )
            last_order_status_history = self.order_status_history_controller.get_last_status_history_by_order_id(
                order_id_to_be_checked
            )
            chef_assigned = self.chef_controller.get_by_id(
                order_to_be_checked.assigned_chef_id
            )
            order_ingredients = self.order_controller.get_order_ingredients_by_order_id(
                order_id_to_be_checked
            )
            order_estimate_time = compute_order_estimated_time(
                order_ingredients, chef_assigned
            )
            date_time_now_milliseconds = get_unix_time_stamp_milliseconds(
                datetime.now()
            )
            order_estimate_time_milliseconds = get_unix_time_stamp_milliseconds(
                last_order_status_history.from_time
                + timedelta(seconds=order_estimate_time)
            )
            if date_time_now_milliseconds > order_estimate_time_milliseconds:
                self._order_send_to_complete(order_to_be_checked)
            else:
                self.order_manager.add_to_queue(order_to_be_checked)

    def _assign_to_chef_and_send_to_in_process(
        self, order_to_be_assign, available_chef_id
    ):
        order_to_be_assign.assigned_chef_id = available_chef_id
        order_to_be_assign.status = OrderStatus.IN_PROCESS
        self.order_controller.reduce_order_ingredients_from_inventory(
            order_to_be_assign.id
        )
        self.order_controller.update_by_id(order_to_be_assign.id, order_to_be_assign)
        self.order_status_history_controller.set_next_status_history_by_order_id(
            order_to_be_assign.id, order_to_be_assign.status
        )
        self.order_manager.add_to_queue(order_to_be_assign)
        print(f"order {order_to_be_assign.id} in process at {datetime.now()}")

    def _order_send_to_cancel(self, order_to_be_cancel):
        order_to_be_cancel.status = OrderStatus.CANCELLED
        self.order_controller.update_by_id(order_to_be_cancel.id, order_to_be_cancel)
        self.order_status_history_controller.set_next_status_history_by_order_id(
            order_to_be_cancel.id, order_to_be_cancel.status
        )
        self.order_manager.add_to_queue(order_to_be_cancel)
        print(f"order {order_to_be_cancel.id} cancelled at {datetime.now()}")

    def _order_send_to_complete(self, order_to_be_complete):
        order_to_be_complete.status = OrderStatus.COMPLETED
        order_to_be_complete.assigned_chef_id = None
        self.order_controller.update_by_id(
            order_to_be_complete.id, order_to_be_complete
        )
        self.order_status_history_controller.set_next_status_history_by_order_id(
            order_to_be_complete.id, order_to_be_complete.status
        )
        self.order_manager.add_to_queue(order_to_be_complete)
        print(f"order {order_to_be_complete.id} completed at {datetime.now()}")
