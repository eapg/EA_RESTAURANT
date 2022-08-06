# structure for the ioc to have just one instance

from src.api.controllers.chef_controller import ChefController
from src.api.controllers.ingredient_controller import IngredientController
from src.api.controllers.inventory_controller import InventoryController
from src.api.controllers.inventory_ingredient_controller import \
    InventoryIngredientController
from src.api.controllers.order_controller import OrderController
from src.api.controllers.order_detail_controller import OrderDetailController
from src.api.controllers.order_status_history_controller import \
    OrderStatusHistoryController
from src.api.controllers.product_controller import ProductController
from src.api.controllers.product_ingredient_controller import \
    ProductIngredientController
from src.core.order_manager import OrderManager
from src.core.sqlalchemy_config import create_session
from src.lib.repositories.impl.chef_repository_impl import ChefRepositoryImpl
from src.lib.repositories.impl.ingredient_repository_impl import \
    IngredientRepositoryImpl
from src.lib.repositories.impl.inventory_ingredient_repository_impl import \
    InventoryIngredientRepositoryImpl
from src.lib.repositories.impl.inventory_repository_impl import \
    InventoryRepositoryImpl
from src.lib.repositories.impl.order_detail_repository_impl import \
    OrderDetailRepositoryImpl
from src.lib.repositories.impl.order_repository_impl import OrderRepositoryImpl
from src.lib.repositories.impl.order_status_history_repository_impl import \
    OrderStatusHistoryRepositoryImpl
from src.lib.repositories.impl.product_ingredient_repository_impl import \
    ProductIngredientRepositoryImpl
from src.lib.repositories.impl.product_repository_impl import \
    ProductRepositoryImpl


def init_sqlalchemy_session(ioc_instance):
    ioc_instance["sqlalchemy_session"] = create_session()


def init_order_manager(ioc_instance):
    ioc_instance["order_manager"] = OrderManager()


def init_repositories(ioc_instance):
    ioc_instance["product_ingredient_repository"] = ProductIngredientRepositoryImpl()
    ioc_instance["product_repository"] = ProductRepositoryImpl()
    ioc_instance["ingredient_repository"] = IngredientRepositoryImpl()
    ioc_instance["inventory_ingredient_repository"] = InventoryIngredientRepositoryImpl(
        ioc_instance["product_ingredient_repository"]
    )
    ioc_instance["order_detail_repository"] = OrderDetailRepositoryImpl()
    ioc_instance["inventory_repository"] = InventoryRepositoryImpl()
    ioc_instance["order_repository"] = OrderRepositoryImpl(
        ioc_instance["order_detail_repository"],
        ioc_instance["product_ingredient_repository"],
        ioc_instance["inventory_ingredient_repository"],
    )

    ioc_instance["chef_repository"] = ChefRepositoryImpl()
    ioc_instance["chef_repository"] = ChefRepositoryImpl(
        ioc_instance["order_repository"]
    )

    ioc_instance["order_status_history_repository"] = OrderStatusHistoryRepositoryImpl()


def init_controllers(ioc_instance):
    ioc_instance["product_ingredient_controller"] = ProductIngredientController(
        ioc_instance["product_ingredient_repository"]
    )
    ioc_instance["product_controller"] = ProductController(
        ioc_instance["product_repository"]
    )
    ioc_instance["ingredient_controller"] = IngredientController(
        ioc_instance["ingredient_repository"]
    )
    ioc_instance["inventory_ingredient_controller"] = InventoryIngredientController(
        ioc_instance["inventory_ingredient_repository"]
    )
    ioc_instance["inventory_controller"] = InventoryController(
        ioc_instance["inventory_repository"]
    )
    ioc_instance["order_controller"] = OrderController(ioc_instance["order_repository"])
    ioc_instance["order_detail_controller"] = OrderDetailController(
        ioc_instance["order_detail_repository"]
    )
    ioc_instance["chef_controller"] = ChefController(ioc_instance["chef_repository"])
    ioc_instance["order_status_history_controller"] = OrderStatusHistoryController(
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
