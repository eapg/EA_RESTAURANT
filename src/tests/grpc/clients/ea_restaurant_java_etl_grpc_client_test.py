import unittest
from unittest import mock

from src.grpc.clients.grpc_client import GrpcClient
from src.grpc.clients.ea_restaurant_java_etl_grpc_client import (
    EaRestaurantJavaEtlGrpcClient,
)
from src.tests.utils.fixtures.grpc_fixture import build_login_client_response


class EaRestaurantJavaEtlGrpcClientTest(unittest.TestCase):
    @mock.patch("src.grpc.clients.grpc_client.java_etl_grpc_client_pb2_grpc")
    @mock.patch("src.grpc.clients.grpc_client.grpc")
    def setUp(self, mocked_grpc, mocked_java_etl_grpc_client_pb2_grpc):
        self.host = "localhost"
        self.server_port = 9090
        self.grpc_client = GrpcClient(self.host, self.server_port)
        self.ea_restaurant_java_etl = EaRestaurantJavaEtlGrpcClient(self.grpc_client)
        self.mocked_grpc = mocked_grpc
        self.mocked_java_etl_grpc_client_pb2_grpc = mocked_java_etl_grpc_client_pb2_grpc

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
