from src.constants.http import HttpStatus
from src.constants.oauth2 import Roles, Scopes
from src.tests.e2e.base_flask_setup_test import BaseFlaskSetupTest
from src.tests.utils.fixtures.json_entities_fixture import build_order_detail
from src.tests.utils.fixtures.token_fixture import build_user_access_token


class OrderDetailApiE2ETest(BaseFlaskSetupTest):
    def after_base_setup(self):
        access_token = build_user_access_token(
            roles=Roles.ADMINISTRATOR.value, scopes=[Scopes.WRITE.value]
        )
        self.headers = {"Authorization": "access_token " + access_token}

    def test_add_order_detail_request(self):
        json_order_detail = build_order_detail()
        request = self.client.post("/order_details", headers=self.headers, json=json_order_detail)
        json_order_detail["id"] = 1
        self.assertEqual(request.get_json(), json_order_detail)

    def test_get_by_id_request_successfully(self):
        json_order_detail = build_order_detail()
        order_detail_1 = self.client.post("/order_details", headers=self.headers, json=json_order_detail)
        request = self.client.get("/order_details/1", headers=self.headers,)
        self.assertEqual(request.get_json(), order_detail_1.get_json())

    def test_get_all_order_detail_request_successfully(self):
        json_order_detail_1 = build_order_detail(order_detail_id=1)
        json_order_detail_2 = build_order_detail(order_detail_id=2)
        json_order_detail_3 = build_order_detail(order_detail_id=3)
        order_detail_1 = self.client.post("/order_details", headers=self.headers, json=json_order_detail_1)
        order_detail_2 = self.client.post("/order_details", headers=self.headers, json=json_order_detail_2)
        order_detail_3 = self.client.post("/order_details", headers=self.headers, json=json_order_detail_3)

        request = self.client.get("/order_details", headers=self.headers,)

        self.assertEqual(
            request.get_json(),
            [
                order_detail_1.get_json(),
                order_detail_2.get_json(),
                order_detail_3.get_json(),
            ],
        )

    def test_updated_order_detail_request_successfully(self):
        json_order_detail = build_order_detail()
        self.client.post("/order_details", headers=self.headers, json=json_order_detail)
        order_detail_with_parameter_updated = {"quantity": 5, "updated_by": 2}
        request = self.client.put(
            "/order_details/1", headers=self.headers, json=order_detail_with_parameter_updated
        )
        request_updated_parameter = request.get_json()
        self.assertEqual(5, request_updated_parameter["quantity"])

    def test_deleted_order_detail_request_successfully(self):
        json_order_detail = build_order_detail()
        self.client.post("/order_details", headers=self.headers, json=json_order_detail)
        request = self.client.delete("/order_details/1", headers=self.headers, json={"updated_by": 3})
        self.assertEqual(request.status_code, HttpStatus.OK.value)

    def test_get_by_ingredient_id_request_successfully(self):
        json_order_detail = build_order_detail()
        order_detail_1 = self.client.post("/order_details", headers=self.headers, json=json_order_detail)
        request = self.client.get("/order_details/by_order_id/1", headers=self.headers,)
        self.assertEqual(request.get_json(), [order_detail_1.get_json()])
