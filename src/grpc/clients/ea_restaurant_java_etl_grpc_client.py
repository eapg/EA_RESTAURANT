from injector import Module, inject


from src.constants.grpc_status import StatusCode
from src.proto import java_etl_grpc_client_pb2
from src.utils.grpc_util import (
    generate_basic_token_from_credentials,
    map_mongo_order_status_histories_to_grpc_mongo_order_status_histories,
    generate_bearer_token_from_access_token,
)
from src.proto import java_etl_grpc_client_pb2_grpc


class EaRestaurantJavaEtlGrpcClient(Module):
    def __init__(self, grpc_client, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
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
        self.access_token = None
        self.refresh_token = None
        self.first_time_login = False
        self.mongo_uuids = None

    def _login_client(self, client_id, client_secret):
        basic_token = generate_basic_token_from_credentials(client_id, client_secret)
        metadata = (("authorization", basic_token),)
        no_param_req = java_etl_grpc_client_pb2.NotParametersRequest()
        login_response = self.oauth2_service_stub.loginClient(
            no_param_req, metadata=metadata
        )
        self.access_token = login_response.accessToken
        self.refresh_token = login_response.refreshToken

    def _refresh_token(self, refresh_token, access_token, client_id, client_secret):
        refresh_token_request = java_etl_grpc_client_pb2.RefreshTokenRequest(
            refreshToken=refresh_token,
            accessToken=access_token,
            clientId=client_id,
            clientSecret=client_secret,
        )
        refresh_token_response = self.oauth2_service_stub.refreshToken(
            refresh_token_request
        )
        self.access_token = refresh_token_response.accessToken

    def insert_mongo_order_status_histories_from_python_etl(
        self, mongo_order_status_histories
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

        def run_grpc_call(metadata):

            return self.mongo_order_status_service_stub.insertMongoOrderStatusHistoriesFromPythonEtl(
                mongo_order_status_histories_request, metadata=metadata
            )

        response = self._run_with_oauth2(run_grpc_call)

        return response.uuids

    def _run_with_oauth2(self, grpc_call, should_refresh_token=False):

        if should_refresh_token:
            try:
                self._refresh_token(
                    self.refresh_token,
                    self.access_token,
                    self.client_id,
                    self.client_secret,
                )

            except Exception as e:

                error_code_value, _ignored = e.code().value
                if error_code_value != StatusCode.PERMISSION_DENIED.value:
                    raise e
                self.access_token = None

        if not self.access_token:
            self._login_client(
                self.client_id,
                self.client_secret,
            )

        metadata = (
            (
                "authorization",
                generate_bearer_token_from_access_token(self.access_token),
            ),
        )

        try:

            return grpc_call(metadata)

        except Exception as e:

            error_code_value, _ignored = e.code().value
            if error_code_value != StatusCode.PERMISSION_DENIED.value:
                raise e
            return self._run_with_oauth2(grpc_call, True)
