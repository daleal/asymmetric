from asymmetric.constants import (
    OPENAPI_SPEC_ROUTE,
    REDOC_DOCUMENTATION_ROUTE,
    SWAGGER_DOCUMENTATION_ROUTE,
)
from asymmetric.openapi.helpers import type_to_string


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
