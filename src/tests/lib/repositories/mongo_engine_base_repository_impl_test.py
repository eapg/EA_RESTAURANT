import unittest
from abc import abstractmethod
from unittest import mock

from mongoengine import connect, disconnect


class MongoEngineBaseRepositoryTestCase(unittest.TestCase):
    @mock.patch(
        "src.core.di_config.mongo_engine_connection",
        return_value=connect("mongoenginetest", host="mongomock://localhost"),
    )
    def setUp(self, mocked_mongo_client):
        self.mocked_mongo_client = mocked_mongo_client

        self.after_base_setup()

    @abstractmethod
    def after_base_setup(self):
        disconnect(alias="mongoenginetest")
        self.mocked_mongo_client.reset_mock()
