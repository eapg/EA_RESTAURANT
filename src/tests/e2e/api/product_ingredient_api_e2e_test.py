from src.constants.http import HttpStatus
from src.constants.oauth2 import Roles, Scopes
from src.tests.e2e.base_flask_setup_test import BaseFlaskSetupTest
from src.tests.utils.fixtures.json_entities_fixture import build_product_ingredient
from src.tests.utils.fixtures.token_fixture import build_user_access_token


class ProductIngredientApiE2ETest(BaseFlaskSetupTest):
    def after_base_setup(self):
        access_token = build_user_access_token(
            roles=Roles.ADMINISTRATOR.value, scopes=[Scopes.WRITE.value]
        )
        self.headers = {"Authorization": "access_token " + access_token}

    def test_add_product_ingredient_request(self):
        json_product_ingredient = build_product_ingredient()
        request = self.client.post("/product_ingredients", headers=self.headers, json=json_product_ingredient)
        json_product_ingredient["id"] = 1
        self.assertEqual(request.get_json(), json_product_ingredient)

    def test_get_by_id_request_successfully(self):
        json_product_ingredient = build_product_ingredient()
        product_ingredient_1 = self.client.post(
            "/product_ingredients", headers=self.headers, json=json_product_ingredient
        )
        request = self.client.get("/product_ingredients/1", headers=self.headers,)
        self.assertEqual(request.get_json(), product_ingredient_1.get_json())

    def test_get_all_product_ingredient_request_successfully(self):
        json_product_ingredient_1 = build_product_ingredient(product_ingredient_id=1)
        json_product_ingredient_2 = build_product_ingredient(product_ingredient_id=2)
        json_product_ingredient_3 = build_product_ingredient(product_ingredient_id=3)
        product_ingredient_1 = self.client.post(
            "/product_ingredients", headers=self.headers, json=json_product_ingredient_1
        )
        product_ingredient_2 = self.client.post(
            "/product_ingredients", headers=self.headers, json=json_product_ingredient_2
        )
        product_ingredient_3 = self.client.post(
            "/product_ingredients", headers=self.headers, json=json_product_ingredient_3
        )

        request = self.client.get("/product_ingredients", headers=self.headers,)

        self.assertEqual(
            request.get_json(),
            [
                product_ingredient_1.get_json(),
                product_ingredient_2.get_json(),
                product_ingredient_3.get_json(),
            ],
        )

    def test_updated_product_ingredient_request_successfully(self):
        json_product_ingredient = build_product_ingredient()
        self.client.post("/product_ingredients", headers=self.headers, json=json_product_ingredient)
        product_ingredient_with_parameter_updated = {
            "cooking_type": "BAKING",
            "updated_by": 2,
        }
        request = self.client.put(
            "/product_ingredients/1", headers=self.headers, json=product_ingredient_with_parameter_updated
        )
        request_updated_parameter = request.get_json()
        self.assertEqual("BAKING", request_updated_parameter["cooking_type"])

    def test_deleted_product_ingredient_request_successfully(self):
        json_product_ingredient = build_product_ingredient()
        self.client.post("/product_ingredients", headers=self.headers, json=json_product_ingredient)
        request = self.client.delete("/product_ingredients/1", headers=self.headers, json={"updated_by": 3})
        self.assertEqual(request.status_code, HttpStatus.OK.value)

    def test_get_by_product_id_request_successfully(self):
        json_product_ingredient = build_product_ingredient()
        product_ingredient_1 = self.client.post(
            "/product_ingredients", headers=self.headers, json=json_product_ingredient
        )
        request = self.client.get("/product_ingredients/by_product_id/1", headers=self.headers,)
        self.assertEqual(request.get_json(), [product_ingredient_1.get_json()])
