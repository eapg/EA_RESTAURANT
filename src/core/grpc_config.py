from src.env_config import get_env_config_instance
from src.grpc.clients.ea_restaurant_java_etl_grpc_client import (
    EaRestaurantJavaEtlGrpcClient,
)
from src.grpc.clients.grpc_client import GrpcClient


def get_ea_restaurant_java_etl_grpc_client():
    env_config = get_env_config_instance()

    grpc_client = GrpcClient(
        env_config.ea_restaurant_java_etl_grpc_host,
        env_config.ea_restaurant_java_etl_grpc_server_port,
    )
    ea_restaurant_java_etl_grpc_client = EaRestaurantJavaEtlGrpcClient(
        grpc_client=grpc_client,
        client_id=env_config.ea_restaurant_java_etl_grpc_client_id,
        client_secret=env_config.ea_restaurant_java_etl_grpc_client_secret,
    )
    return ea_restaurant_java_etl_grpc_client
