# structure for the ioc to have just one instance

from src.api.controllers import (
    chef_controller,
    ingredient_controller,
    inventory_controller,
    inventory_ingredient_controller,
    order_controller,
    order_detail_controller,
    order_status_history_controller,
    product_controller,
    product_ingredient_controller,
)
from src.core import order_manager, sqlalchemy_config
from src.lib.repositories.impl import (
    chef_repository_impl,
    ingredient_repository_impl,
    inventory_ingredient_repository_impl,
    inventory_repository_impl,
    order_detail_repository_impl,
    order_repository_impl,
    order_status_history_repository_impl,
    product_ingredient_repository_impl,
    product_repository_impl,
)


def init_sqlalchemy_session(ioc_instance):
    ioc_instance["sqlalchemy_session"] = sqlalchemy_config.create_session()


def init_order_manager(ioc_instance):
    ioc_instance["order_manager"] = order_manager.OrderManager()


def init_repositories(ioc_instance):
    ioc_instance[
        "product_ingredient_repository"
    ] = product_ingredient_repository_impl.ProductIngredientRepositoryImpl()
    ioc_instance["product_repository"] = product_repository_impl.ProductRepositoryImpl()
    ioc_instance[
        "ingredient_repository"
    ] = ingredient_repository_impl.IngredientRepositoryImpl()
    ioc_instance[
        "inventory_ingredient_repository"
    ] = inventory_ingredient_repository_impl.InventoryIngredientRepositoryImpl(
        ioc_instance["product_ingredient_repository"]
    )
    ioc_instance[
        "order_detail_repository"
    ] = order_detail_repository_impl.OrderDetailRepositoryImpl()
    ioc_instance[
        "inventory_repository"
    ] = inventory_repository_impl.InventoryRepositoryImpl()
    ioc_instance["order_repository"] = order_repository_impl.OrderRepositoryImpl(
        ioc_instance["order_detail_repository"],
        ioc_instance["product_ingredient_repository"],
        ioc_instance["inventory_ingredient_repository"],
    )

    ioc_instance["chef_repository"] = chef_repository_impl.ChefRepositoryImpl(
        ioc_instance["order_repository"]
    )

    ioc_instance[
        "order_status_history_repository"
    ] = order_status_history_repository_impl.OrderStatusHistoryRepositoryImpl()


def init_controllers(ioc_instance):
    ioc_instance[
        "product_ingredient_controller"
    ] = product_ingredient_controller.ProductIngredientController(
        ioc_instance["product_ingredient_repository"]
    )
    ioc_instance["product_controller"] = product_controller.ProductController(
        ioc_instance["product_repository"]
    )
    ioc_instance["ingredient_controller"] = ingredient_controller.IngredientController(
        ioc_instance["ingredient_repository"]
    )
    ioc_instance[
        "inventory_ingredient_controller"
    ] = inventory_ingredient_controller.InventoryIngredientController(
        ioc_instance["inventory_ingredient_repository"]
    )
    ioc_instance["inventory_controller"] = inventory_controller.InventoryController(
        ioc_instance["inventory_repository"]
    )
    ioc_instance["order_controller"] = order_controller.OrderController(
        ioc_instance["order_repository"]
    )
    ioc_instance[
        "order_detail_controller"
    ] = order_detail_controller.OrderDetailController(
        ioc_instance["order_detail_repository"]
    )
    ioc_instance["chef_controller"] = chef_controller.ChefController(
        ioc_instance["chef_repository"]
    )
    ioc_instance[
        "order_status_history_controller"
    ] = order_status_history_controller.OrderStatusHistoryController(
        ioc_instance["order_status_history_repository"]
    )


class Ioc:
    def __init__(self):
        self._ioc_instance = {}
        init_sqlalchemy_session(self._ioc_instance)
        init_order_manager(self._ioc_instance)
        init_repositories(self._ioc_instance)
        init_controllers(self._ioc_instance)

    def get_instance(self, instance_id):
        return self._ioc_instance[instance_id]


IOC_CONTEXT_MAP = {"ioc_instance": None}


def get_ioc_instance():

    if not IOC_CONTEXT_MAP["ioc_instance"]:
        IOC_CONTEXT_MAP["ioc_instance"] = Ioc()

    return IOC_CONTEXT_MAP["ioc_instance"]
