

class Request:
    def __init__(self, url_rule=None, method=None, headers=None):
        self.url_rule = url_rule
        self.method = method
        self.headers = headers


def create_request(url, method, access_token):

    request = Request(
        url_rule=url, method=method, headers={"Authorization": "access_token " + access_token}
    )

    return request
