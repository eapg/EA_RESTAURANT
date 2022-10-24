from abc import ABCMeta
from datetime import datetime, timedelta

from src.api.controllers.chef_controller import ChefController
from src.api.controllers.order_controller import OrderController
from src.constants.audit import InternalUsers
from src.constants.order_status import OrderStatus
from src.core.engine.processors.abstract_processor import AbstractProcessor
from src.core.order_manager import ORDER_QUEUE_STATUS_TO_CHUNK_LIMIT_MAP
from src.lib.repositories.impl_no_sql.order_status_history_repository_impl import (
    OrderStatusHistoryRepositoryImpl as MongoOrderStatusHistoryRepository,
)
from src.utils.order_util import compute_order_estimated_time
from src.utils.time_util import get_unix_time_stamp_milliseconds


def initialize_kitchen_simulator(app_processor_config, app_context):
    ioc = app_context.ioc
    order_controller = ioc.get(OrderController)
    order_manager = app_processor_config.order_manager

    load_order_into_order_manager(
        order_manager, order_controller, OrderStatus.NEW_ORDER
    )
    load_order_into_order_manager(
        order_manager, order_controller, OrderStatus.IN_PROCESS
    )
    load_order_into_order_manager(
        order_manager, order_controller, OrderStatus.COMPLETED
    )
    load_order_into_order_manager(
        order_manager, order_controller, OrderStatus.CANCELLED
    )


def load_order_into_order_manager(order_manager, order_controller, order_status):
    orders = order_controller.get_orders_by_status(
        order_status.name,
        order_limit=ORDER_QUEUE_STATUS_TO_CHUNK_LIMIT_MAP[order_status],
    )

    if orders:
        for order in orders:
            order_manager.add_to_queue(order)


class KitchenSimulator(AbstractProcessor, metaclass=ABCMeta):
    def __init__(self, app_processor_config, app_context=None):
        super().__init__(
            app_processor_config=app_processor_config, app_context=app_context
        )
        self._process_clean_queues_delta_time_sum = 0  # float
        self._process_clean_queues_timeout = 60  # seconds
        self.order_manager = None
        self.chef_controller = None
        self.mongo_order_status_history_repository = None
        self.order_controller = None

    def set_app_context(self, app_context):
        ioc = app_context.ioc
        self.order_controller = ioc.get(OrderController)
        self.mongo_order_status_history_repository = ioc.get(
            MongoOrderStatusHistoryRepository
        )
        self.chef_controller = ioc.get(ChefController)
        self.order_manager = self.app_processor_config.order_manager
        self.app_context = app_context

    def process(self, delta_time):
        self.process_new_orders()
        self.process_orders_in_process()
        self.process_clean_queues(delta_time)

    def process_new_orders(self):

        orders_to_process = self.order_controller.get_orders_by_status(
            OrderStatus.NEW_ORDER.name,
            order_limit=ORDER_QUEUE_STATUS_TO_CHUNK_LIMIT_MAP[OrderStatus.NEW_ORDER],
        )
        orders_validation_map = self.order_controller.get_validated_orders_map(
            orders_to_process
        )
        available_chef = self.chef_controller.get_available_chefs()

        if available_chef:

            order_in_turn_id = self.order_manager.get_queue_from_status(
                OrderStatus.NEW_ORDER.name
            )

            if order_in_turn_id:
                order_to_be_assigned = list(
                    filter(
                        (lambda order: order.id == order_in_turn_id), orders_to_process
                    )
                )

                if orders_validation_map[order_to_be_assigned[0].id]:
                    self._assign_to_chef_and_send_to_in_process(
                        order_to_be_assigned[0], available_chef[0]
                    )

                else:
                    self._order_send_to_cancel(order_to_be_assigned[0])

    def process_orders_in_process(self):

        order_id_to_be_checked = self.order_manager.get_queue_from_status(
            OrderStatus.IN_PROCESS.name
        )

        if order_id_to_be_checked:
            order_to_be_checked = self.order_controller.get_by_id(
                order_id_to_be_checked
            )
            last_order_status_history = self.mongo_order_status_history_repository.get_last_status_history_by_order_id(
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

    def process_clean_queues(self, delta_time):
        self._process_clean_queues_delta_time_sum += delta_time

        if (
            self._process_clean_queues_delta_time_sum
            > self._process_clean_queues_timeout
        ):
            self.order_manager.clean_queues_with_full_storage()
            self._process_clean_queues_delta_time_sum = 0

    def _assign_to_chef_and_send_to_in_process(
        self, order_to_be_assign, available_chef
    ):
        order_to_be_assign.assigned_chef_id = available_chef.id
        print(f"chef {available_chef.id} assigned to order {order_to_be_assign.id}")
        order_to_be_assign.status = OrderStatus.IN_PROCESS.name
        self.order_controller.reduce_order_ingredients_from_inventory(
            order_to_be_assign.id
        )
        order_to_be_assign.update_by = InternalUsers.KITCHEN_SIMULATOR
        self.order_controller.update_by_id(order_to_be_assign.id, order_to_be_assign)
        self.mongo_order_status_history_repository.set_next_status_history_by_order_id(
            order_to_be_assign.id, order_to_be_assign.status
        )
        self.order_manager.add_to_queue(order_to_be_assign)
        print(f"order {order_to_be_assign.id} in process at {datetime.now()}")

    def _order_send_to_cancel(self, order_to_be_cancel):
        order_to_be_cancel.status = OrderStatus.CANCELLED.name
        self.order_controller.update_by_id(order_to_be_cancel.id, order_to_be_cancel)
        self.mongo_order_status_history_repository.set_next_status_history_by_order_id(
            order_to_be_cancel.id, order_to_be_cancel.status
        )
        self.order_manager.add_to_queue(order_to_be_cancel)
        print(f"order {order_to_be_cancel.id} cancelled at {datetime.now()}")

    def _order_send_to_complete(self, order_to_be_complete):
        order_to_be_complete.status = OrderStatus.COMPLETED.name
        self.order_controller.update_by_id(
            order_to_be_complete.id, order_to_be_complete
        )
        self.mongo_order_status_history_repository.set_next_status_history_by_order_id(
            order_to_be_complete.id, order_to_be_complete.status
        )
        self.order_manager.add_to_queue(order_to_be_complete)
        print(f"order {order_to_be_complete.id} completed at {datetime.now()}")
