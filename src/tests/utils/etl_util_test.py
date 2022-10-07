import unittest
from src.lib.entities.mongo_engine_odm_mapping import (
    OrderStatusHistory as MongoOrderStatusHistory,
)
from src.lib.entities.sqlalchemy_orm_mapping import OrderStatusHistory
from src.utils.etl_util import (
    convert_mongo_order_status_history_to_postgres_order_status_history,
)


class TestEtlUtil(unittest.TestCase):
    def test_convert_mongo_order_status_history_to_postgres_order_status_history(self):
        mongo_order_status_history = MongoOrderStatusHistory()
        mongo_order_status_history.order_id = 5

        order_status_history = OrderStatusHistory()

        order_status_history_returned = (
            convert_mongo_order_status_history_to_postgres_order_status_history(
                mongo_order_status_history, order_status_history
            )
        )

        self.assertEqual(
            mongo_order_status_history.order_id, order_status_history_returned.order_id
        )
        self.assertEqual(
            type(order_status_history_returned), type(OrderStatusHistory())
        )
