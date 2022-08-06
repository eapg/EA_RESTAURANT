from unittest import mock


class QueryOperationsMock:
    def __init__(self, mocked_query):
        self.mocked_query = mocked_query
        self.current_mock = self.mocked_query

    def filter(self, return_value=None, side_effect_fn=None):
        mocked_filter = mock.Mock()
        self.current_mock.return_value = mocked_filter
        mocked_filter.filter = mock.Mock()
        mocked_filter.filter.return_value = return_value or mocked_filter.filter.return_value
        mocked_filter.filter.side_effect = side_effect_fn or mocked_filter.filter.side_effect
        self.current_mock = mocked_filter.filter
        return self

    def first(self, return_value=None, side_effect_fn=None):
        mocked_first = mock.Mock()
        self.current_mock.return_value = mocked_first
        mocked_first.first = mock.Mock()
        mocked_first.first.return_value = return_value or mocked_first.first.return_value
        mocked_first.first.side_effect = side_effect_fn or mocked_first.first.side_effect
        self.current_mock = mocked_first.first
        return self

    def exists(self, return_value=None, side_effect_fn=None):
        mocked_exists = mock.Mock()
        self.current_mock.return_value = mocked_exists
        mocked_exists.exists = mock.Mock()
        mocked_exists.exists.return_value = return_value or mocked_exists.exists.return_value
        mocked_exists.exists.side_effect = side_effect_fn or mocked_exists.exists.side_effect
        self.current_mock = mocked_exists.exists
        return self

    def update(self, return_value=None, side_effect_fn=None):
        mocked_update = mock.Mock()
        self.current_mock.return_value = mocked_update
        mocked_update.update = mock.Mock()
        mocked_update.update.return_value = return_value or mocked_update.update.return_value
        mocked_update.update.side_effect = side_effect_fn or mocked_update.update.side_effect
        self.current_mock = mocked_update.update
        return self

    def get_mocked_query(self):
        return self.mocked_query


class QueryMock:
    def __init__(self, mocked_session=None):
        self.mocked_session = mocked_session or mock.Mock()
        self.current_mock = self.mocked_session

    def query(self, return_value=None, side_effect_fn=None):
        mocked_query = mock.Mock()
        mocked_query.return_value = return_value or mocked_query.return_value
        mocked_query.side_effect = side_effect_fn or mocked_query.side_effect
        self.current_mock.query = mocked_query
        self.current_mock = mocked_query
        return QueryOperationsMock(mocked_query)
