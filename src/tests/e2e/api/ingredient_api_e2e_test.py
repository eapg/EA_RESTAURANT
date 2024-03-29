from src.constants.http import HttpStatus
from src.constants.oauth2 import Roles, Scopes
from src.tests.e2e.base_flask_setup_test import BaseFlaskSetupTest
from src.tests.utils.fixtures.json_entities_fixture import build_ingredient
from src.tests.utils.fixtures.token_fixture import build_user_access_token


class IngredientApiE2ETest(BaseFlaskSetupTest):
    def after_base_setup(self):
        access_token = build_user_access_token(
            roles=Roles.ADMINISTRATOR.value, scopes=[Scopes.WRITE.value]
        )
        self.headers = {"Authorization": "access_token " + access_token}

    def test_add_ingredient_request(self):
        json_ingredient = build_ingredient()
        request = self.client.post("/ingredients", headers=self.headers, json=json_ingredient)
        json_ingredient["id"] = 1
        self.assertEqual(request.get_json(), json_ingredient)

    def test_get_by_id_request_successfully(self):
        json_ingredient = build_ingredient()
        ingredient_1 = self.client.post("/ingredients", headers=self.headers, json=json_ingredient)
        request = self.client.get("/ingredients/1", headers=self.headers)
        self.assertEqual(request.get_json(), ingredient_1.get_json())

    def test_get_all_ingredient_request_successfully(self):
        json_ingredient_1 = build_ingredient(ingredient_id=1)
        json_ingredient_2 = build_ingredient(ingredient_id=2)
        json_ingredient_3 = build_ingredient(ingredient_id=3)
        ingredient_1 = self.client.post("/ingredients", headers=self.headers, json=json_ingredient_1)
        ingredient_2 = self.client.post("/ingredients", headers=self.headers, json=json_ingredient_2)
        ingredient_3 = self.client.post("/ingredients", headers=self.headers, json=json_ingredient_3)

        request = self.client.get("/ingredients", headers=self.headers)

        self.assertEqual(
            request.get_json(),
            [ingredient_1.get_json(), ingredient_2.get_json(), ingredient_3.get_json()],
        )

    def test_updated_ingredient_request_successfully(self):
        json_ingredient = build_ingredient()
        self.client.post("/ingredients", headers=self.headers, json=json_ingredient)
        ingredient_with_parameter_updated = {"name": "test 2", "updated_by": 2}
        request = self.client.put(
            "/ingredients/1", headers=self.headers, json=ingredient_with_parameter_updated
        )
        request_updated_parameter = request.get_json()
        self.assertEqual("test 2", request_updated_parameter["name"])

    def test_deleted_ingredient_request_successfully(self):
        json_ingredient = build_ingredient()
        self.client.post("/ingredients", headers=self.headers, json=json_ingredient)
        request = self.client.delete("/ingredients/1", headers=self.headers, json={"updated_by": 3})
        self.assertEqual(request.status_code, HttpStatus.OK.value)
