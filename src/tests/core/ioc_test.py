import unittest

from src.core import ioc


class IocTestCase(unittest.TestCase):
    def test_instance_not_none(self):

        ioc_instance_1 = ioc.get_ioc_instance()

        self.assertIsNotNone(ioc_instance_1)

    def test_same_instance(self):

        ioc_instance_1 = ioc.get_ioc_instance()
        ioc_instance_2 = ioc.get_ioc_instance()

        self.assertEqual(ioc_instance_1, ioc_instance_2)
