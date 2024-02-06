from src.utils.utils import equals


class SecuredHttpRequestUrl:
    def __init__(self, path=None, method=None):
        self.path = path
        self.method = method

    def __eq__(self, other):
        return equals(self, other)

    def __hash__(self):
        return hash((self.path, self.method))
