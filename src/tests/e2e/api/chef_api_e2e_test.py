from src.constants.http import HttpStatus
from src.constants.oauth2 import Roles, Scopes
from src.tests.e2e.base_flask_setup_test import BaseFlaskSetupTest
from src.tests.utils.fixtures.json_entities_fixture import build_chef
from src.tests.utils.fixtures.mapping_orm_fixtures import create_order_with_procedure
from src.tests.utils.fixtures.token_fixture import build_user_access_token


class ChefApiE2ETest(BaseFlaskSetupTest):
    def after_base_setup(self):
        access_token = build_user_access_token(
            roles=Roles.ADMINISTRATOR.value, scopes=[Scopes.READ_WRITE.value]
        )
        self.headers = {"Authorization": "access_token " + access_token}

    def test_add_chef_request(self):
        json_chef = build_chef()
        request = self.client.post("/chefs", headers=self.headers, json=json_chef)
        json_chef["id"] = 1
        self.assertEqual(request.get_json(), json_chef)

    def test_get_by_id_request_successfully(self):
        json_chef = build_chef()
        chef_1 = self.client.post("/chefs", headers=self.headers, json=json_chef)
        request = self.client.get("/chefs/1", headers=self.headers)
        self.assertEqual(request.get_json(), chef_1.get_json())

    def test_get_all_chef_request_successfully(self):
        json_chef_1 = build_chef(chef_id=1)
        json_chef_2 = build_chef(chef_id=2)
        json_chef_3 = build_chef(chef_id=3)
        chef_1 = self.client.post("/chefs", headers=self.headers, json=json_chef_1)
        chef_2 = self.client.post("/chefs", headers=self.headers, json=json_chef_2)
        chef_3 = self.client.post("/chefs", headers=self.headers, json=json_chef_3)

        request = self.client.get("/chefs", headers=self.headers)

        self.assertEqual(
            request.get_json(),
            [chef_1.get_json(), chef_2.get_json(), chef_3.get_json()],
        )

    def test_updated_chef_request_successfully(self):
        json_chef = build_chef()
        self.client.post("/chefs", headers=self.headers, json=json_chef)
        chef_with_parameter_updated = {"skill": 10, "updated_by": 2}
        request = self.client.put(
            "/chefs/1",
            headers=self.headers,
            json=chef_with_parameter_updated,
        )
        request_updated_parameter = request.get_json()
        self.assertEqual(10, request_updated_parameter["skill"])

    def test_deleted_chef_request_successfully(self):
        json_chef = build_chef()
        self.client.post("/chefs", headers=self.headers, json=json_chef)
        request = self.client.delete(
            "/chefs/1",
            headers=self.headers,
            json={"updated_by": 3},
        )
        self.assertEqual(request.status_code, HttpStatus.OK.value)

    def test_get_available_chef_request_successfully(self):
        json_chef_1 = build_chef(chef_id=1)
        json_chef_2 = build_chef(chef_id=2)
        create_order_with_procedure(
            engine=self.engine, assigned_chef_id=1, order_status="IN_PROCESS"
        )
        self.client.post("/chefs", headers=self.headers, json=json_chef_1)
        chef_2 = self.client.post("/chefs", headers=self.headers, json=json_chef_2)
        request = self.client.get("/chefs/available", headers=self.headers)
        self.assertEqual(request.get_json(), [chef_2.get_json()])
