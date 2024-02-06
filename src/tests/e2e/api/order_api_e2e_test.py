from src.constants.http import HttpStatus
from src.constants.oauth2 import Scopes, Roles
from src.tests.e2e.base_flask_setup_test import BaseFlaskSetupTest
from src.tests.utils.fixtures.json_entities_fixture import build_order
from src.tests.utils.fixtures.mapping_orm_fixtures import (
    create_order_detail_with_procedure,
    create_product_ingredient_with_procedure,
)
from src.tests.utils.fixtures.token_fixture import build_user_access_token


class OrderApiE2ETest(BaseFlaskSetupTest):
    def after_base_setup(self):
        access_token = build_user_access_token(
            roles=Roles.ADMINISTRATOR.value, scopes=[Scopes.WRITE.value]
        )
        self.headers = {"Authorization": "access_token " + access_token}

    def test_add_order_request(self):
        json_order = build_order()
        request = self.client.post("/orders", headers=self.headers, json=json_order)
        json_order["id"] = 1
        self.assertEqual(request.get_json(), json_order)

    def test_get_by_id_request_successfully(self):
        json_order = build_order()
        order_1 = self.client.post("/orders", headers=self.headers, json=json_order)
        request = self.client.get("/orders/1", headers=self.headers,)
        self.assertEqual(request.get_json(), order_1.get_json())

    def test_get_all_order_request_successfully(self):
        json_order_1 = build_order(order_id=1)
        json_order_2 = build_order(order_id=2)
        json_order_3 = build_order(order_id=3)
        order_1 = self.client.post("/orders", headers=self.headers, json=json_order_1)
        order_2 = self.client.post("/orders", headers=self.headers, json=json_order_2)
        order_3 = self.client.post("/orders", headers=self.headers, json=json_order_3)

        request = self.client.get("/orders", headers=self.headers)

        self.assertEqual(
            request.get_json(),
            [order_1.get_json(), order_2.get_json(), order_3.get_json()],
        )

    def test_updated_order_request_successfully(self):
        json_order = build_order()
        self.client.post("/orders", headers=self.headers, json=json_order)
        order_with_parameter_updated = {"status": "IN_PROCESS", "updated_by": 2}
        request = self.client.put("/orders/1", headers=self.headers, json=order_with_parameter_updated)
        request_updated_parameter = request.get_json()
        self.assertEqual("IN_PROCESS", request_updated_parameter["status"])

    def test_deleted_order_request_successfully(self):
        json_order = build_order()
        self.client.post("/orders", headers=self.headers, json=json_order)
        request = self.client.delete("/orders/1", headers=self.headers, json={"updated_by": 3})
        self.assertEqual(request.status_code, HttpStatus.OK.value)

    def test_orders_by_status_request_successfully(self):
        json_order = build_order(status="IN_PROCESS")
        order_1 = self.client.post("/orders", headers=self.headers, json=json_order)
        request = self.client.get(
            "/orders/by_order_status/IN_PROCESS?limit=10", headers=self.headers, json=json_order
        )
        self.assertEqual(request.get_json(), [order_1.get_json()])

    def test_get_order_ingredients_by_order_id(self):
        create_order_detail_with_procedure(self.engine, order_id=1, product_id=12)
        create_product_ingredient_with_procedure(self.engine, product_id=12)
        json_order = build_order(order_id=1, status="IN_PROCESS")
        self.client.post("/orders", headers=self.headers, json=json_order)
        request = self.client.get("/orders/1/ingredients", headers=self.headers, json=json_order)
        order_ingredients = request.get_json()
        self.assertEqual(order_ingredients[0]["product_id"], 12)
