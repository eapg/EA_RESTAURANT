# structure for the ioc to have just one instance

from src.api.controllers import *
from src.lib.repositories.impl import *


class Ioc:
    def __init__(self):
        self._instance_ioc = {}
        self._init_repositories()
        self._init_controllers()

    def _init_repositories(self):
        self._instance_ioc[
            "product_repository"
        ] = product_repository_impl.ProductRepositoryImpl()
        self._instance_ioc[
            "ingredient_repository"
        ] = ingredient_repository_impl.IngredientRepositoryImpl()
        self._instance_ioc[
            "inventory_ingredient_repository"
        ] = inventory_ingredient_repository_impl.InventoryIngredientRepositoryImpl()
        self._instance_ioc[
            "inventory_repository"
        ] = inventory_repository_impl.InventoryRepositoryImpl(self._instance_ioc[
            "inventory_ingredient_repository"])
        self._instance_ioc[
            "order_repository"
        ] = order_repository_impl.OrderRepositoryImpl()
        self._instance_ioc[
            "order_detail_repository"
        ] = order_detail_repository_impl.OrderDetailRepositoryImpl()
        self._instance_ioc[
            "chef_repository"
        ] = chef_repository_impl.ChefRepositoryImpl()

    def _init_controllers(self):
        self._instance_ioc["product_controller"] = product_controller.ProductController(
            self._instance_ioc["product_repository"]
        )
        self._instance_ioc[
            "ingredient_controller"
        ] = ingredient_controller.IngredientController(
            self._instance_ioc["ingredient_repository"]
        )
        self._instance_ioc[
            "inventory_ingredient_controller"
        ] = inventory_ingredient_controller.InventoryIngredientController(
            self._instance_ioc["inventory_ingredient_repository"]
        )
        self._instance_ioc[
            "inventory_controller"
        ] = inventory_controller.InventoryController(
            self._instance_ioc["inventory_repository"]
        )
        self._instance_ioc["order_controller"] = order_controller.OrderController(
            self._instance_ioc["order_repository"]
        )
        self._instance_ioc[
            "order_detail_controller"
        ] = order_detail_controller.OrderDetailController(
            self._instance_ioc["order_detail_repository"]
        )
        self._instance_ioc["chef_controller"] = chef_controller.ChefController(
            self._instance_ioc["chef_repository"]
        )

    def get_instance(self, instance_id):
        return self._instance_ioc[instance_id]


ioc_instance = Ioc()


def get_ioc_instance():
    return ioc_instance
