import unittest

from src.tests.utils.fixtures.chef_fixture import build_chef
from src.tests.utils.fixtures.order_fixture import build_order
from src.utils.order_util import array_chef_to_chef_assigned_orders_map_reducer


class TestOrderUtil(unittest.TestCase):
    def test_array_chef_to_chef_assigned_orders_map_reducer(self):

        chef_principal = build_chef(chef_id=1, name="Elido p", chef_skills=5)

        order_1 = build_order(assigned_chef_id=chef_principal.id)
        order_2 = build_order(assigned_chef_id=None)
        order_3 = build_order(assigned_chef_id=chef_principal.id)

        orders = [order_1, order_2, order_3]

        chefs_with_assigned_orders_map = {}

        chefs_with_assigned_orders_map = array_chef_to_chef_assigned_orders_map_reducer(
            chefs_with_assigned_orders_map, chef_principal.id, orders
        )
        self.assertEqual(chefs_with_assigned_orders_map[1], [order_1, order_3])
