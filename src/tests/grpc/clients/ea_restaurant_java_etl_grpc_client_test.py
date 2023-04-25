import unittest
from unittest import mock

from src.grpc.clients.ea_restaurant_java_etl_grpc_client import (
    EaRestaurantJavaEtlGrpcClient,
)
from src.grpc.clients.grpc_client import GrpcClient
from src.tests.utils.fixtures.grpc_fixture import (
    build_login_client_response,
    build_refresh_token_request,
)
from src.tests.utils.fixtures.mapping_odm_fixtures import build_order_status_history


class EaRestaurantJavaEtlGrpcClientTest(unittest.TestCase):
    @mock.patch(
        "src.grpc.clients.ea_restaurant_java_etl_grpc_client.java_etl_grpc_client_pb2_grpc"
    )
    @mock.patch("src.grpc.clients.grpc_client.grpc")
    def setUp(self, mocked_grpc, mocked_java_etl_grpc_client_pb2_grpc):
        self.host = "localhost"
        self.server_port = 9090
        self.grpc_client = GrpcClient(self.host, self.server_port)
        self.ea_restaurant_java_etl = EaRestaurantJavaEtlGrpcClient(self.grpc_client)
        self.mocked_grpc = mocked_grpc
        self.mocked_java_etl_grpc_client_pb2_grpc = mocked_java_etl_grpc_client_pb2_grpc
        self.path = ""

    def tearDown(self):
        self.mocked_grpc.reset_mock()
        self.mocked_java_etl_grpc_client_pb2_grpc.reset_mock()

    @mock.patch(
        "src.grpc.clients.ea_restaurant_java_etl_grpc_client.generate_basic_token_from_credentials"
    )
    def test_client_login_with_grpc_client(
        self, mocked_generate_basic_token_with_credentials
    ):

        client_login_response = build_login_client_response()
        mocked_generate_basic_token_with_credentials.return_value = "basic token test"
        self.mocked_java_etl_grpc_client_pb2_grpc.Oauth2ServiceStub().loginClient.return_value = (
            client_login_response
        )
        credentials = self.ea_restaurant_java_etl.login_client(
            "postman001", "postmansecret01"
        )
        mocked_generate_basic_token_with_credentials.assert_called_with(
            "postman001", "postmansecret01"
        )
        self.assertEqual(credentials, client_login_response)

    def test_client_refresh_token_with_grpc_client(self):
        refresh_token_response = build_login_client_response()
        refresh_token_request = build_refresh_token_request()
        self.mocked_java_etl_grpc_client_pb2_grpc.Oauth2ServiceStub().refreshToken.return_value = (
            refresh_token_response
        )
        refresh_token_response_returned = self.ea_restaurant_java_etl.refresh_token(
            "test refresh token", "test access token", "postman001", "postmansecret01"
        )
        self.assertEqual(refresh_token_response_returned, refresh_token_response)
        self.mocked_java_etl_grpc_client_pb2_grpc.Oauth2ServiceStub().refreshToken.assert_called_with(
            refresh_token_request
        )

    @mock.patch(
        "src.grpc.clients.ea_restaurant_java_etl_grpc_client.map_mongo_order_status_histories_to_grpc_mongo_order_status_histories"
    )
    def test_insert_mongo_order_status_histories_from_python_etl(
        self, mocked_map_mongo_order_status_to_grpc_mongo_order_status
    ):
        mongo_order_status_history_1 = build_order_status_history(
            id="64481d50959f4c4df51c77cf"
        )
        mongo_order_status_history_2 = build_order_status_history(
            id="64481d50959f4c4df51c77ce"
        )
        mongo_order_status_histories = [
            mongo_order_status_history_1,
            mongo_order_status_history_2,
        ]
        access_token = "this is a test token"
        uuids_to_be_returned = ["64481d50959f4c4df51c77cf", "64481d50959f4c4df51c77ce"]
        self.mocked_java_etl_grpc_client_pb2_grpc.MongoOrderStatusHistoryServiceStub().insertMongoOrderStatusHistoriesFromPythonEtl.return_value = (
            uuids_to_be_returned
        )
        uuids_returned = self.ea_restaurant_java_etl.insert_mongo_order_status_histories_from_python_etl(
            mongo_order_status_histories, access_token
        )
        self.assertEqual(uuids_returned, uuids_to_be_returned)
        mocked_map_mongo_order_status_to_grpc_mongo_order_status.assert_called_with(
            mongo_order_status_histories
        )
