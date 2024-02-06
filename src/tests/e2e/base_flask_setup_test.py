from abc import abstractmethod

from flask import Flask
from src.core.sqlalchemy_config import get_engine
from src.flask.api_setup import setup_api
from src.lib.entities.sqlalchemy_orm_mapping import Base
from src.tests.base_env_config_test import BaseEnvConfigTest


def clean_database(engine):
    meta = Base.metadata
    for table in meta.sorted_tables:
        engine.execute(f"TRUNCATE {table} RESTART IDENTITY CASCADE;")


class BaseFlaskSetupTest(BaseEnvConfigTest):
    def setUp(self):
        super().setUp()
        self.engine = get_engine()
        self.app = setup_api(Flask(__name__))
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.after_base_setup()

    def tearDown(self):
        clean_database(self.engine)
        self.app_context.pop()

    @abstractmethod
    def after_base_setup(self):
        pass
