from src.proto import java_etl_grpc_client_pb2
from src.utils.grpc_util import (
    generate_basic_token_from_credentials,
    map_mongo_order_status_histories_to_grpc_mongo_order_status_histories,
)
from src.proto import java_etl_grpc_client_pb2_grpc


class EaRestaurantJavaEtlGrpcClient:
    def __init__(self, grpc_client):
        self.grpc_client = grpc_client
        self.channel = grpc_client.get_channel()
        self.oauth2_service_stub = java_etl_grpc_client_pb2_grpc.Oauth2ServiceStub(
            self.channel
        )
        self.mongo_order_status_service_stub = (
            java_etl_grpc_client_pb2_grpc.MongoOrderStatusHistoryServiceStub(
                self.channel
            )
        )

    def login_client(self, client_id, client_secret):
        basic_token = generate_basic_token_from_credentials(client_id, client_secret)
        metadata = (("authorization", basic_token),)
        no_param = java_etl_grpc_client_pb2.NotParametersRequest()
        return self.oauth2_service_stub.loginClient(no_param, metadata=metadata)

    def refresh_token(self, refresh_token, access_token, client_id, client_secret):
        refresh_token_request = java_etl_grpc_client_pb2.RefreshTokenRequest(
            refreshToken=refresh_token,
            accessToken=access_token,
            clientId=client_id,
            clientSecret=client_secret,
        )
        return self.oauth2_service_stub.refreshToken(refresh_token_request)

    def insert_mongo_order_status_histories_from_python_etl(
        self, mongo_order_status_histories, access_token
    ):
        mongo_order_status_histories = (
            map_mongo_order_status_histories_to_grpc_mongo_order_status_histories(
                mongo_order_status_histories
            )
        )
        mongo_order_status_histories_request = (
            java_etl_grpc_client_pb2.MongoOrderStatusHistoriesFromPythonRequest(
                mongoOrderStatusHistory=mongo_order_status_histories
            )
        )
        metadata = (("authorization", access_token),)
        return self.mongo_order_status_service_stub.insertMongoOrderStatusHistoriesFromPythonEtl(
            mongo_order_status_histories_request, metadata=metadata
        )
