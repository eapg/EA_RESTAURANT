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


class Ioc:
    def __init__(self):
        self._instance_ioc = {}
        self._init_order_manager()
        self._init_repositories()
        self._init_controllers()

    def _init_order_manager(self):
        self._instance_ioc["order_manager"] = OrderManager()

    def _init_repositories(self):
        self._instance_ioc[
            "product_ingredient_repository"
        ] = ProductIngredientRepositoryImpl()
        self._instance_ioc["product_repository"] = ProductRepositoryImpl()
        self._instance_ioc["ingredient_repository"] = IngredientRepositoryImpl()
        self._instance_ioc[
            "inventory_ingredient_repository"
        ] = InventoryIngredientRepositoryImpl(
            self._instance_ioc["product_ingredient_repository"]
        )
        self._instance_ioc["order_detail_repository"] = OrderDetailRepositoryImpl()
        self._instance_ioc["inventory_repository"] = InventoryRepositoryImpl()
        self._instance_ioc["order_repository"] = OrderRepositoryImpl(
            self._instance_ioc["order_detail_repository"],
            self._instance_ioc["product_ingredient_repository"],
            self._instance_ioc["inventory_ingredient_repository"],
        )

        self._instance_ioc["chef_repository"] = ChefRepositoryImpl()
        self._instance_ioc["chef_repository"] = ChefRepositoryImpl(
            self._instance_ioc["order_repository"]
        )

        self._instance_ioc[
            "order_status_history_repository"
        ] = OrderStatusHistoryRepositoryImpl()

    def _init_controllers(self):
        self._instance_ioc[
            "product_ingredient_controller"
        ] = ProductIngredientController(
            self._instance_ioc["product_ingredient_repository"]
        )
        self._instance_ioc["product_controller"] = ProductController(
            self._instance_ioc["product_repository"]
        )
        self._instance_ioc["ingredient_controller"] = IngredientController(
            self._instance_ioc["ingredient_repository"]
        )
        self._instance_ioc[
            "inventory_ingredient_controller"
        ] = InventoryIngredientController(
            self._instance_ioc["inventory_ingredient_repository"]
        )
        self._instance_ioc["inventory_controller"] = InventoryController(
            self._instance_ioc["inventory_repository"]
        )
        self._instance_ioc["order_controller"] = OrderController(
            self._instance_ioc["order_repository"]
        )
        self._instance_ioc["order_detail_controller"] = OrderDetailController(
            self._instance_ioc["order_detail_repository"]
        )
        self._instance_ioc["chef_controller"] = ChefController(
            self._instance_ioc["chef_repository"]
        )
        self._instance_ioc[
            "order_status_history_controller"
        ] = OrderStatusHistoryController(
            self._instance_ioc["order_status_history_repository"]
        )

    def get_instance(self, instance_id):
        return self._instance_ioc[instance_id]


ioc_instance = Ioc()


def get_ioc_instance():
    return ioc_instance
