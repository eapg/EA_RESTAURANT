from src.constants.http import HttpStatus
from src.constants.oauth2 import Roles, Scopes
from src.tests.e2e.base_flask_setup_test import BaseFlaskSetupTest
from src.tests.utils.fixtures.json_entities_fixture import build_inventory
from src.tests.utils.fixtures.token_fixture import build_user_access_token


class InventoryApiE2ETest(BaseFlaskSetupTest):
    def after_base_setup(self):
        access_token = build_user_access_token(
            roles=Roles.ADMINISTRATOR.value, scopes=[Scopes.WRITE.value]
        )
        self.headers = {"Authorization": "access_token " + access_token}

    def test_add_inventory_request(self):
        json_inventory = build_inventory()
        request = self.client.post(
            "/inventories", headers=self.headers, json=json_inventory
        )
        json_inventory["id"] = 1
        self.assertEqual(request.get_json(), json_inventory)

    def test_get_by_id_request_successfully(self):
        json_inventory = build_inventory()
        inventory_1 = self.client.post(
            "/inventories", headers=self.headers, json=json_inventory
        )
        request = self.client.get("/inventories/1", headers=self.headers)
        self.assertEqual(request.get_json(), inventory_1.get_json())

    def test_get_all_inventory_request_successfully(self):
        json_inventory_1 = build_inventory(inventory_id=1)
        json_inventory_2 = build_inventory(inventory_id=2)
        json_inventory_3 = build_inventory(inventory_id=3)
        inventory_1 = self.client.post(
            "/inventories", headers=self.headers, json=json_inventory_1
        )
        inventory_2 = self.client.post(
            "/inventories", headers=self.headers, json=json_inventory_2
        )
        inventory_3 = self.client.post(
            "/inventories", headers=self.headers, json=json_inventory_3
        )

        request = self.client.get("/inventories", headers=self.headers)

        self.assertEqual(
            request.get_json(),
            [inventory_1.get_json(), inventory_2.get_json(), inventory_3.get_json()],
        )

    def test_updated_inventory_request_successfully(self):
        json_inventory = build_inventory()
        self.client.post("/inventories", headers=self.headers, json=json_inventory)
        inventory_with_parameter_updated = {"name": "test 2", "updated_by": 2}
        request = self.client.put(
            "/inventories/1",
            headers=self.headers,
            json=inventory_with_parameter_updated,
        )
        request_updated_parameter = request.get_json()
        self.assertEqual("test 2", request_updated_parameter["name"])

    def test_deleted_inventory_request_successfully(self):
        json_inventory = build_inventory()
        self.client.post("/inventories", headers=self.headers, json=json_inventory)
        request = self.client.delete(
            "/inventories/1", headers=self.headers, json={"updated_by": 3}
        )
        self.assertEqual(request.status_code, HttpStatus.OK.value)
