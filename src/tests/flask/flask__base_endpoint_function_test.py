import unittest
from abc import abstractmethod

from injector import Injector

from src.core.di_config import DiProviders
from src.env_config import get_env_config_instance
from src.tests.base_env_config_test import BaseEnvConfigTest


class FlaskBaseEndpointFunctionTest(BaseEnvConfigTest):

    def setUp(self):
        super().setUp()
        self.env_config = get_env_config_instance()
        self.ioc = Injector(DiProviders)
        self.after_base_setup()

    @abstractmethod
    def after_base_setup(self):
        pass
