from src.constants.http import HttpStatus
from src.constants.oauth2 import Roles, Scopes
from src.tests.e2e.base_flask_setup_test import BaseFlaskSetupTest
from src.tests.utils.fixtures.json_entities_fixture import build_product
from src.tests.utils.fixtures.token_fixture import build_user_access_token


class ProductApiE2ETest(BaseFlaskSetupTest):
    def after_base_setup(self):
        access_token = build_user_access_token(
            roles=Roles.ADMINISTRATOR.value, scopes=[Scopes.WRITE.value]
        )
        self.headers = {"Authorization": "access_token " + access_token}

    def test_add_product_request(self):
        json_product = build_product()
        request = self.client.post("/products", headers=self.headers, json=json_product)
        json_product["id"] = 1
        self.assertEqual(request.get_json(), json_product)

    def test_get_by_id_request_successfully(self):
        json_product = build_product()
        product_1 = self.client.post(
            "/products", headers=self.headers, json=json_product
        )
        request = self.client.get(
            "/products/1",
            headers=self.headers,
        )
        self.assertEqual(request.get_json(), product_1.get_json())

    def test_get_all_product_request_successfully(self):
        json_product_1 = build_product(product_id=1)
        json_product_2 = build_product(product_id=2)
        json_product_3 = build_product(product_id=3)
        product_1 = self.client.post(
            "/products", headers=self.headers, json=json_product_1
        )
        product_2 = self.client.post(
            "/products", headers=self.headers, json=json_product_2
        )
        product_3 = self.client.post(
            "/products", headers=self.headers, json=json_product_3
        )

        request = self.client.get(
            "/products",
            headers=self.headers,
        )

        self.assertEqual(
            request.get_json(),
            [product_1.get_json(), product_2.get_json(), product_3.get_json()],
        )

    def test_updated_product_request_successfully(self):
        json_product = build_product()
        self.client.post("/products", headers=self.headers, json=json_product)
        product_with_parameter_updated = {"name": "test 2", "updated_by": 2}
        request = self.client.put(
            "/products/1", headers=self.headers, json=product_with_parameter_updated
        )
        request_updated_parameter = request.get_json()
        self.assertEqual("test 2", request_updated_parameter["name"])

    def test_deleted_product_request_successfully(self):
        json_product = build_product()
        self.client.post("/products", headers=self.headers, json=json_product)
        request = self.client.delete(
            "/products/1", headers=self.headers, json={"updated_by": 3}
        )
        self.assertEqual(request.status_code, HttpStatus.OK.value)
