import unittest

from src.env_config import get_env_config_instance


class BaseEnvConfigTest(unittest.TestCase):
    def setUp(self):
        self.env_config = get_env_config_instance()
