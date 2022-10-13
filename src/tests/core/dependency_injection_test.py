import unittest
from unittest import mock

from injector import Injector

from src.api.controllers.chef_controller import ChefController
from src.core.di_config import DiProviders
from src.lib.repositories.impl_v2.chef_repository_impl import ChefRepositoryImpl


class DependencyInjectionTest(unittest.TestCase):

    def test_dependency_injection_single_instance(self):
        injector = Injector(DiProviders)
        chef_controller_1 = injector.get(ChefController)
        chef_controller_2 = injector.get(ChefController)
        self.assertEqual(chef_controller_1, chef_controller_2)

    @mock.patch("src.core.di_config.get_engine")
    def test_engine_injection_successfully(self, mocked_get_engine):

        injector = Injector(DiProviders)
        chef_repository = injector.get(ChefRepositoryImpl)
        self.assertEqual(mocked_get_engine(), chef_repository.engine)
