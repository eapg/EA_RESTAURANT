import unittest
from abc import abstractmethod
from unittest import mock
from mongoengine import connect, disconnect

mocked_mongo_engine_connection = mock.Mock(
    return_value=connect("mongoenginetest", host="mongomock://localhost")
)


def mocked_init_mongo_engine_connection_impl(ioc_instance):
    ioc_instance["mongo_engine_connection"] = mocked_mongo_engine_connection


class MongoEngineBaseRepositoryTestCase(unittest.TestCase):
    @mock.patch("src.core.ioc.init_mongo_engine_connection")
    def setUp(self, mocked_init_mongo_engine_connection):
        self.mocked_mongo_engine_connection = mocked_mongo_engine_connection
        mocked_init_mongo_engine_connection.return_value = mock.Mock()
        mocked_init_mongo_engine_connection.side_effect = (
            mocked_init_mongo_engine_connection_impl
        )
        self.mocked_init_mongo_engine_connection = mocked_init_mongo_engine_connection

        self.after_base_setup()

    @abstractmethod
    def after_base_setup(self):
        disconnect(alias="mongoenginetest")
        self.mocked_mongo_engine_connection.reset_mock()
