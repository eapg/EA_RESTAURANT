from src.constants.http import HttpStatus
from src.constants.oauth2 import Roles, Scopes
from src.tests.e2e.base_flask_setup_test import BaseFlaskSetupTest
from src.tests.utils.fixtures.json_entities_fixture import build_inventory_ingredient
from src.tests.utils.fixtures.token_fixture import build_user_access_token


class InventoryIngredientApiE2ETest(BaseFlaskSetupTest):
    def after_base_setup(self):
        access_token = build_user_access_token(
            roles=Roles.ADMINISTRATOR.value, scopes=[Scopes.WRITE.value]
        )
        self.headers = {"Authorization": "access_token " + access_token}

    def test_add_inventory_ingredient_request(self):
        json_inventory_ingredient = build_inventory_ingredient()
        request = self.client.post(
            "/inventory_ingredients", headers=self.headers, json=json_inventory_ingredient
        )
        json_inventory_ingredient["id"] = 1
        self.assertEqual(request.get_json(), json_inventory_ingredient)

    def test_get_by_id_request_successfully(self):
        json_inventory_ingredient = build_inventory_ingredient()
        inventory_ingredient_1 = self.client.post(
            "/inventory_ingredients", headers=self.headers, json=json_inventory_ingredient
        )
        request = self.client.get("/inventory_ingredients/1", headers=self.headers)
        self.assertEqual(request.get_json(), inventory_ingredient_1.get_json())

    def test_get_all_inventory_ingredient_request_successfully(self):
        json_inventory_ingredient_1 = build_inventory_ingredient(
            inventory_ingredient_id=1
        )
        json_inventory_ingredient_2 = build_inventory_ingredient(
            inventory_ingredient_id=2
        )
        json_inventory_ingredient_3 = build_inventory_ingredient(
            inventory_ingredient_id=3
        )
        inventory_ingredient_1 = self.client.post(
            "/inventory_ingredients", headers=self.headers, json=json_inventory_ingredient_1
        )
        inventory_ingredient_2 = self.client.post(
            "/inventory_ingredients", headers=self.headers, json=json_inventory_ingredient_2
        )
        inventory_ingredient_3 = self.client.post(
            "/inventory_ingredients", headers=self.headers, json=json_inventory_ingredient_3
        )

        request = self.client.get("/inventory_ingredients", headers=self.headers,)

        self.assertEqual(
            request.get_json(),
            [
                inventory_ingredient_1.get_json(),
                inventory_ingredient_2.get_json(),
                inventory_ingredient_3.get_json(),
            ],
        )

    def test_updated_inventory_ingredient_request_successfully(self):
        json_inventory_ingredient = build_inventory_ingredient()
        self.client.post("/inventory_ingredients", headers=self.headers, json=json_inventory_ingredient)
        inventory_ingredient_with_parameter_updated = {"quantity": 5, "updated_by": 2}
        request = self.client.put(
            "/inventory_ingredients/1", headers=self.headers, json=inventory_ingredient_with_parameter_updated
        )
        request_updated_parameter = request.get_json()
        self.assertEqual(5, request_updated_parameter["quantity"])

    def test_deleted_inventory_ingredient_request_successfully(self):
        json_inventory_ingredient = build_inventory_ingredient()
        self.client.post("/inventory_ingredients", headers=self.headers, json=json_inventory_ingredient)
        request = self.client.delete("/inventory_ingredients/1", headers=self.headers, json={"updated_by": 3})
        self.assertEqual(request.status_code, HttpStatus.OK.value)

    def test_get_by_ingredient_id_request_successfully(self):
        json_inventory_ingredient = build_inventory_ingredient()
        inventory_ingredient_1 = self.client.post(
            "/inventory_ingredients", headers=self.headers, json=json_inventory_ingredient
        )
        request = self.client.get("/inventory_ingredients/by_ingredient_id/1", headers=self.headers)
        self.assertEqual(request.get_json(), [inventory_ingredient_1.get_json()])
