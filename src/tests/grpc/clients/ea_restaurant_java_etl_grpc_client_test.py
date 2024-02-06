import unittest
from unittest import mock

import grpc

from src.env_config import get_env_config_instance
from src.exceptions.exceptions import GrpcPermissionDeniedException
from src.grpc.clients.ea_restaurant_java_etl_grpc_client import (
    EaRestaurantJavaEtlGrpcClient,
)
from src.grpc.clients.grpc_client import GrpcClient
from src.tests.utils.fixtures.grpc_fixture import (
    build_login_client_response,
    build_grpc_mongo_order_status_history,
    build_uuids_response,
    build_refresh_token_response,
    build_refresh_token_request,
)
from src.tests.utils.fixtures.mapping_odm_fixtures import build_order_status_history

raise_exception_for_java_etl_client_insert_mongo_order_status_histories_from_python_etl_side_effect = (
    True
)


def java_etl_client_insert_mongo_order_status_histories_from_python_etl_side_effect(
    mongo_order_status_histories_request, metadata=None
):
    uuids_to_be_returned = build_uuids_response(
        ["63656f20f2a8a6a247ae31cc", "63656f20f2a8a6a247ae31cd"]
    )
    global raise_exception_for_java_etl_client_insert_mongo_order_status_histories_from_python_etl_side_effect

    if (
        metadata[0][1] == "Bearer test access token"
        and raise_exception_for_java_etl_client_insert_mongo_order_status_histories_from_python_etl_side_effect
    ):
        e = GrpcPermissionDeniedException(grpc.StatusCode.PERMISSION_DENIED)
        raise_exception_for_java_etl_client_insert_mongo_order_status_histories_from_python_etl_side_effect = (
            False
        )
        raise e
    else:
        return uuids_to_be_returned


def java_etl_client_refresh_token_side_effect(refresh_token_request=None):
    e = GrpcPermissionDeniedException(grpc.StatusCode.PERMISSION_DENIED)
    raise e


class EaRestaurantJavaEtlGrpcClientTest(unittest.TestCase):
    @mock.patch(
        "src.grpc.clients.ea_restaurant_java_etl_grpc_client.java_etl_grpc_client_pb2_grpc"
    )
    @mock.patch("src.grpc.clients.grpc_client.grpc")
    def setUp(self, mocked_grpc, mocked_java_etl_grpc_client_pb2_grpc):
        self.env_config_for_testing = get_env_config_instance()
        self.client_id = (
            self.env_config_for_testing.ea_restaurant_java_etl_grpc_client_id
        )
        self.client_secret = (
            self.env_config_for_testing.ea_restaurant_java_etl_grpc_client_secret
        )
        self.host = "localhost"
        self.server_port = 9090
        self.grpc_client = GrpcClient(self.host, self.server_port)
        self.ea_restaurant_java_etl = EaRestaurantJavaEtlGrpcClient(
            self.grpc_client, self.client_id, self.client_secret
        )
        self.mocked_grpc = mocked_grpc
        self.mocked_java_etl_grpc_client_pb2_grpc = mocked_java_etl_grpc_client_pb2_grpc
        self.mocked_oauth2_service_stub = (
            self.mocked_java_etl_grpc_client_pb2_grpc.Oauth2ServiceStub()
        )
        self.mongo_order_status_histories = [
            build_order_status_history(id="63656f20f2a8a6a247ae31cc"),
            build_order_status_history(id="63656f20f2a8a6a247ae31cd"),
        ]
        self.mapped_mongo_order_status_histories = [
            build_grpc_mongo_order_status_history(id="63656f20f2a8a6a247ae31cc"),
            build_grpc_mongo_order_status_history(id="63656f20f2a8a6a247ae31cd"),
        ]
        self.mocked_java_etl_grpc_client_pb2_grpc.MongoOrderStatusHistoriesFromPythonRequest.return_value = (
            self.mapped_mongo_order_status_histories
        )
        self.mocked_mongo_order_status_service_stub = (
            self.mocked_java_etl_grpc_client_pb2_grpc.MongoOrderStatusHistoryServiceStub()
        )

    def tearDown(self):
        self.mocked_grpc.reset_mock()
        self.mocked_java_etl_grpc_client_pb2_grpc.reset_mock()
        self.mocked_oauth2_service_stub.reset_mock()

    @mock.patch(
        "src.grpc.clients.ea_restaurant_java_etl_grpc_client.map_mongo_order_status_histories_to_grpc_mongo_order_status_histories"
    )
    def test_insert_mongo_order_status_histories_from_python_etl_with_oauth2_auth_login(
        self, mocked_map_mongo_order_status_to_grpc_mongo_order_status
    ):
        uuids_to_be_returned = build_uuids_response(
            ["63656f20f2a8a6a247ae31cc", "63656f20f2a8a6a247ae31cd"]
        )
        self.mocked_mongo_order_status_service_stub.insertMongoOrderStatusHistoriesFromPythonEtl.return_value = (
            uuids_to_be_returned
        )
        mocked_map_mongo_order_status_to_grpc_mongo_order_status.return_value = (
            self.mapped_mongo_order_status_histories
        )
        login_response = build_login_client_response()
        self.mocked_oauth2_service_stub.loginClient.return_value = login_response
        uuids = self.ea_restaurant_java_etl.insert_mongo_order_status_histories_from_python_etl(
            self.mongo_order_status_histories
        )

        self.assertEqual(
            self.ea_restaurant_java_etl.access_token, login_response.accessToken
        )
        self.assertEqual(
            self.ea_restaurant_java_etl.refresh_token, login_response.refreshToken
        )

        self.assertEqual(
            uuids, ["63656f20f2a8a6a247ae31cc", "63656f20f2a8a6a247ae31cd"]
        )

    @mock.patch(
        "src.grpc.clients.ea_restaurant_java_etl_grpc_client.map_mongo_order_status_histories_to_grpc_mongo_order_status_histories"
    )
    def test_insert_mongo_order_status_histories_from_python_etl_with_oauth2_auth_with_expired_access_token(
        self, mocked_map_mongo_order_status_to_grpc_mongo_order_status
    ):

        self.mocked_mongo_order_status_service_stub.insertMongoOrderStatusHistoriesFromPythonEtl.side_effect = java_etl_client_insert_mongo_order_status_histories_from_python_etl_side_effect
        login_response = build_login_client_response()
        self.mocked_oauth2_service_stub.loginClient.return_value = login_response
        refresh_token_request = build_refresh_token_request()
        refresh_token_response = build_refresh_token_response()
        self.mocked_oauth2_service_stub.refreshToken.return_value = (
            refresh_token_response
        )
        uuids = self.ea_restaurant_java_etl.insert_mongo_order_status_histories_from_python_etl(
            self.mongo_order_status_histories
        )
        self.mocked_oauth2_service_stub.refreshToken.assert_called_with(
            refresh_token_request
        )
        self.assertEqual(
            uuids, ["63656f20f2a8a6a247ae31cc", "63656f20f2a8a6a247ae31cd"]
        )

    @mock.patch(
        "src.grpc.clients.ea_restaurant_java_etl_grpc_client.map_mongo_order_status_histories_to_grpc_mongo_order_status_histories"
    )
    def test_insert_mongo_order_status_histories_from_python_etl_with_oauth2_auth_with_expired_refresh_token(
        self, mocked_map_mongo_order_status_to_grpc_mongo_order_status
    ):
        self.mocked_mongo_order_status_service_stub.insertMongoOrderStatusHistoriesFromPythonEtl.side_effect = java_etl_client_insert_mongo_order_status_histories_from_python_etl_side_effect
        self.mocked_oauth2_service_stub.refreshToken.side_effect = (
            java_etl_client_refresh_token_side_effect
        )
        login_response = build_login_client_response()
        self.mocked_oauth2_service_stub.loginClient.return_value = login_response

        uuids = self.ea_restaurant_java_etl.insert_mongo_order_status_histories_from_python_etl(
            self.mongo_order_status_histories
        )
        self.assertEqual(
            2, self.mocked_oauth2_service_stub.loginClient._mock_call_count
        )
        self.assertEqual(
            uuids, ["63656f20f2a8a6a247ae31cc", "63656f20f2a8a6a247ae31cd"]
        )
