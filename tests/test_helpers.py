from asymmetric.constants import HTTP_METHODS
from asymmetric.helpers import http_verb


class TestHTTPVerb:
    def setup_method(self):
        self.http_methods = [f" {x.title()} " for x in HTTP_METHODS]

    def test_http_verb_cleaner(self):
        for index, method in enumerate(self.http_methods):
            assert http_verb(method) == HTTP_METHODS[index]
