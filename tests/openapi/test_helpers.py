from asymmetric.constants import (
    OPENAPI_SPEC_ROUTE,
    REDOC_DOCUMENTATION_ROUTE,
    SWAGGER_DOCUMENTATION_ROUTE,
)
from asymmetric.openapi.helpers import type_to_string, is_not_docs


class TestTypeToString:
    def test_string_type(self):
        name = type_to_string(str)
        assert name == "string"

    def test_float_type(self):
        name = type_to_string(float)
        assert name == "number"

    def test_integer_type(self):
        name = type_to_string(int)
        assert name == "integer"

    def test_boolean_type(self):
        name = type_to_string(bool)
        assert name == "boolean"

    def test_noen_type_type(self):
        name = type_to_string(type(None))
        assert name == "null"

    def test_list_type(self):
        name = type_to_string(list)
        assert name == "array"

    def test_object_type(self):
        name = type_to_string(object)
        assert name == "object"


class TestIsNotDocs:
    def setup_method(self):
        self.docs = [
            OPENAPI_SPEC_ROUTE,
            REDOC_DOCUMENTATION_ROUTE,
            SWAGGER_DOCUMENTATION_ROUTE,
        ]

        self.not_docs = [
            "/v1/test/route/1",
            "/v1/test/route/2",
            "/v1/test/route/3",
            "/v1/test/route/4",
        ]

    def test_doc_endpoints(self):
        for doc in self.docs:
            assert is_not_docs(doc) is False

    def test_non_doc_endpoints(self):
        for not_doc in self.not_docs:
            assert is_not_docs(not_doc) is True
