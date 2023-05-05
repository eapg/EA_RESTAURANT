from injector import Module, provider, singleton
from pymongo import MongoClient
from sqlalchemy.engine.base import Engine

from src.api.controllers.chef_controller import ChefController
from src.api.controllers.ingredient_controller import IngredientController
from src.api.controllers.inventory_controller import InventoryController
from src.api.controllers.inventory_ingredient_controller import (
    InventoryIngredientController,
)
from src.api.controllers.order_controller import OrderController
from src.api.controllers.order_detail_controller import OrderDetailController
from src.api.controllers.order_status_history_controller import (
    OrderStatusHistoryController,
)
from src.api.controllers.product_controller import ProductController
from src.api.controllers.product_ingredient_controller import (
    ProductIngredientController,
)
from src.core.grpc_config import get_ea_restaurant_java_etl_grpc_client
from src.core.mongo_engine_config import mongo_engine_connection
from src.core.sqlalchemy_config import get_engine
from src.grpc.clients.ea_restaurant_java_etl_grpc_client import (
    EaRestaurantJavaEtlGrpcClient,
)
from src.lib.repositories.chef_repository import ChefRepository
from src.lib.repositories.impl_no_sql.order_status_history_repository_impl import (
    OrderStatusHistoryRepositoryImpl as MongoOrderStatusHistoryRepository,
)
from src.lib.repositories.impl_v2.oauth2_repository_impl import Oauth2RepositoryImpl
from src.lib.repositories.ingredient_repository import IngredientRepository
from src.lib.repositories.inventory_ingredient_repository import (
    InventoryIngredientRepository,
)
from src.lib.repositories.inventory_repository import InventoryRepository
from src.lib.repositories.order_detail_repository import OrderDetailRepository
from src.lib.repositories.order_repository import OrderRepository
from src.lib.repositories.order_status_history_repository import (
    OrderStatusHistoryRepository,
)
from src.lib.repositories.product_ingredient_repository import (
    ProductIngredientRepository,
)
from src.lib.repositories.product_repository import ProductRepository


class DiProviders(Module):
    # pylint: disable=R0201
    @singleton
    @provider
    def get_sqlalchemy_engine(self) -> Engine:
        return get_engine()

    # pylint: disable=R0201
    @singleton
    @provider
    def get_mongo_client(self) -> MongoClient:
        return mongo_engine_connection()

    # pylint: disable=R0201
    @singleton
    @provider
    def get_ea_restaurant_java_etl(self) -> EaRestaurantJavaEtlGrpcClient:
        return get_ea_restaurant_java_etl_grpc_client()

    def configure(self, binder):

        # Repositories
        binder.bind(Oauth2RepositoryImpl, scope=singleton)
        binder.bind(ChefRepository, scope=singleton)
        binder.bind(IngredientRepository, scope=singleton)
        binder.bind(InventoryIngredientRepository, scope=singleton)
        binder.bind(InventoryRepository, scope=singleton)
        binder.bind(OrderDetailRepository, scope=singleton)
        binder.bind(OrderRepository, scope=singleton)
        binder.bind(OrderStatusHistoryRepository, scope=singleton)
        binder.bind(ProductIngredientRepository, scope=singleton)
        binder.bind(ProductRepository, scope=singleton)
        binder.bind(
            OrderStatusHistoryRepository,
            to=MongoOrderStatusHistoryRepository,
            scope=singleton,
        )

        # Controllers
        binder.bind(ChefController, scope=singleton)
        binder.bind(IngredientController, scope=singleton)
        binder.bind(InventoryIngredientController, scope=singleton)
        binder.bind(InventoryController, scope=singleton)
        binder.bind(OrderDetailController, scope=singleton)
        binder.bind(OrderController, scope=singleton)
        binder.bind(OrderStatusHistoryController, scope=singleton)
        binder.bind(ProductIngredientController, scope=singleton)
        binder.bind(ProductController, scope=singleton)

        # grpc_clients
        binder.bind(
            EaRestaurantJavaEtlGrpcClient,
            to=self.get_ea_restaurant_java_etl(),
            scope=singleton,
        )
