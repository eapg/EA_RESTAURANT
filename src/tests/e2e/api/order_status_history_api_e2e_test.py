from src.constants.http_status_code import HttpStatus
from src.tests.e2e.base_flask_setup_test import BaseFlaskSetupTest
from src.tests.utils.fixtures.json_entities_fixture import build_order_status_history


class OrderStatusHistoryApiE2ETest(BaseFlaskSetupTest):
    def after_base_setup(self):
        pass

    def test_add_order_status_history_request(self):
        json_order_status_history = build_order_status_history()
        request = self.client.post(
            "/order_status_histories", json=json_order_status_history
        )
        json_order_status_history["id"] = 1
        self.assertEqual(request.get_json(), json_order_status_history)

    def test_get_by_id_request_successfully(self):
        json_order_status_history = build_order_status_history()
        order_status_history_1 = self.client.post(
            "/order_status_histories", json=json_order_status_history
        )
        request = self.client.get("/order_status_histories/1")
        self.assertEqual(request.get_json(), order_status_history_1.get_json())

    def test_get_all_order_status_history_request_successfully(self):
        json_order_status_history_1 = build_order_status_history(
            order_status_history_id=1
        )
        json_order_status_history_2 = build_order_status_history(
            order_status_history_id=2
        )
        json_order_status_history_3 = build_order_status_history(
            order_status_history_id=3
        )
        order_status_history_1 = self.client.post(
            "/order_status_histories", json=json_order_status_history_1
        )
        order_status_history_2 = self.client.post(
            "/order_status_histories", json=json_order_status_history_2
        )
        order_status_history_3 = self.client.post(
            "/order_status_histories", json=json_order_status_history_3
        )

        request = self.client.get("/order_status_histories")

        self.assertEqual(
            request.get_json(),
            [
                order_status_history_1.get_json(),
                order_status_history_2.get_json(),
                order_status_history_3.get_json(),
            ],
        )

    def test_updated_order_status_history_request_successfully(self):
        json_order_status_history = build_order_status_history()
        self.client.post("/order_status_histories", json=json_order_status_history)
        order_status_history_with_parameter_updated = {
            "to_status": "IN_PROCESS",
            "updated_by": 2,
        }
        request = self.client.put(
            "/order_status_histories/1",
            json=order_status_history_with_parameter_updated,
        )
        request_updated_parameter = request.get_json()
        self.assertEqual("IN_PROCESS", request_updated_parameter["to_status"])

    def test_deleted_order_status_history_request_successfully(self):
        json_order_status_history = build_order_status_history()
        self.client.post("/order_status_histories", json=json_order_status_history)
        request = self.client.delete(
            "/order_status_histories/1", json={"updated_by": 3}
        )
        self.assertEqual(request.status_code, HttpStatus.OK.value)

    def test_get_by_order_id_request_successfully(self):
        json_order_status_history = build_order_status_history()
        order_status_history_1 = self.client.post(
            "/order_status_histories", json=json_order_status_history
        )
        request = self.client.get("/order_status_histories/by_order_id/1")
        self.assertEqual(request.get_json(), [order_status_history_1.get_json()])
