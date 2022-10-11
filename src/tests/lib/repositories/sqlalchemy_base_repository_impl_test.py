import unittest
from abc import abstractmethod
from unittest import mock

mocked_sqlalchemy_engine = mock.Mock()
mocked_sqlalchemy_session = mock.Mock()


def mocked_init_sqlalchemy_session_impl(ioc_instance):
    ioc_instance["sqlalchemy_engine"] = mocked_sqlalchemy_engine


class SqlAlchemyBaseRepositoryTestCase(unittest.TestCase):
    @mock.patch("sqlalchemy.not_")
    @mock.patch("src.core.ioc.init_sqlalchemy_engine")
    def setUp(self, mocked_init_sqlalchemy_engine, mocked_sqlalchemy_not):
        self.mocked_sqlalchemy_session = mocked_sqlalchemy_session
        self.mocked_sqlalchemy_engine = mocked_sqlalchemy_engine

        self.mocked_sqlalchemy_engine.begin.return_value.__enter__ = mock.Mock()
        self.mocked_sqlalchemy_engine.begin.return_value.__exit__ = mock.Mock()

        self.mocked_sqlalchemy_session.begin.return_value.__enter__ = mock.Mock()
        self.mocked_sqlalchemy_session.begin.return_value.__exit__ = mock.Mock()

        mocked_init_sqlalchemy_engine.return_value = mock.Mock()
        mocked_init_sqlalchemy_engine.side_effect = mocked_init_sqlalchemy_session_impl
        self.mocked_init_sqlalchemy_engine = mocked_init_sqlalchemy_engine
        self.mocked_sqlalchemy_not = mocked_sqlalchemy_not

        self.after_base_setup()

    def tearDown(self):
        self.mocked_sqlalchemy_session.reset_mock()
        self.mocked_init_sqlalchemy_engine.reset_mock()

    @abstractmethod
    def after_base_setup(self):
        pass
