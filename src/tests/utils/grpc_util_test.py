import unittest
from unittest import mock

from src.tests.utils.fixtures.mapping_odm_fixtures import build_order_status_history
from src.utils.grpc_util import (
    map_mongo_order_status_histories_to_grpc_mongo_order_status_histories,
)


class TestGrpcUtil(unittest.TestCase):
    @mock.patch("src.utils.grpc_util.get_unix_time_stamp_milliseconds")
    def test_grpc_util_mapped_mongo_order_status_to_grpc_order_status(
        self, mocked_get_unix_time_stamp_milliseconds
    ):
        mongo_order_status_histories = [
            build_order_status_history(id="63656f20f2a8a6a247ae31cc"),
            build_order_status_history(id="63656f20f2a8a6a247ae31cd"),
        ]

        mapped_to_grpc_mongo_order_status_histories = (
            map_mongo_order_status_histories_to_grpc_mongo_order_status_histories(
                mongo_order_status_histories
            )
        )

        self.assertEqual(
            mongo_order_status_histories[0].id,
            mapped_to_grpc_mongo_order_status_histories[0].id,
        )
        self.assertEqual(
            mongo_order_status_histories[0].order_id,
            mapped_to_grpc_mongo_order_status_histories[0].orderId,
        )
        self.assertEqual(
            mongo_order_status_histories[0].from_status,
            mapped_to_grpc_mongo_order_status_histories[0].fromStatus,
        )
        self.assertEqual(
            mongo_order_status_histories[0].entity_status,
            mapped_to_grpc_mongo_order_status_histories[0].entityStatus,
        )
        self.assertEqual(
            mongo_order_status_histories[1].id,
            mapped_to_grpc_mongo_order_status_histories[1].id,
        )
        self.assertEqual(
            mongo_order_status_histories[1].order_id,
            mapped_to_grpc_mongo_order_status_histories[1].orderId,
        )
        self.assertEqual(
            mongo_order_status_histories[1].from_status,
            mapped_to_grpc_mongo_order_status_histories[1].fromStatus,
        )
        self.assertEqual(
            mongo_order_status_histories[1].entity_status,
            mapped_to_grpc_mongo_order_status_histories[1].entityStatus,
        )
