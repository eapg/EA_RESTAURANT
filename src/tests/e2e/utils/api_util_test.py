import unittest
from src.flask.utils.api_util import fetch_class_from_data


from src.lib.entities.chef import Chef


class ApiUtilTest(unittest.TestCase):
    def test_fetch_class_from_data(self):

        data = {"user_id": 1, "skill": 5, "created_by": 1}

        chef_to_fetch = Chef()
        chef = fetch_class_from_data(chef_to_fetch, data)
        self.assertEqual(data["user_id"], chef.user_id)
        self.assertEqual(data["skill"], chef.skill)
        self.assertEqual(data["created_by"], chef.created_by)
