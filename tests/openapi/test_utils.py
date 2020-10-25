from inspect import getfullargspec

from asymmetric.openapi.constants import ANY_TYPE
from asymmetric.openapi.utils import (
    get_defaults_schema,
    get_no_defaults_schema,
    get_parameters_amount,
)


class TestGetParametersAmount:
    def setup_method(self):
        def no_defaults(x, y, z):
            return x + y + z

        def has_defaults(x, y=2, z=3):
            return x + y + z

        def only_defaults(x=1, y=2, z=3):
            return x + y + z

        self.no_defaults_params = getfullargspec(no_defaults)
        self.has_defaults_params = getfullargspec(has_defaults)
        self.only_defaults_params = getfullargspec(only_defaults)

    def test_no_defaults_result(self):
        params_amount = get_parameters_amount(self.no_defaults_params)
        no_defaults = params_amount["no_defaults"]
        defaults = params_amount["defaults"]
        assert no_defaults == 3
        assert defaults == 0

    def test_has_defaults_result(self):
        params_amount = get_parameters_amount(self.has_defaults_params)
        no_defaults = params_amount["no_defaults"]
        defaults = params_amount["defaults"]
        assert no_defaults == 1
        assert defaults == 2

    def test_only_defaults_result(self):
        params_amount = get_parameters_amount(self.only_defaults_params)
        no_defaults = params_amount["no_defaults"]
        defaults = params_amount["defaults"]
        assert no_defaults == 0
        assert defaults == 3


class TestGetNoDefaultsSchema:
    def setup_method(self):
        def no_defaults(x, y, z):
            return x + y + z

        def has_defaults(x, y=2, z=3):
            return x + y + z

        def only_defaults(x=1, y=2, z=3):
            return x + y + z

        def typed_params(x, y: int, z: str, d=3):
            return [x, y, z, d]

        self.no_defaults_params = getfullargspec(no_defaults)
        self.no_defaults_schema = {
            "x": {"oneOf": ANY_TYPE},
            "y": {"oneOf": ANY_TYPE},
            "z": {"oneOf": ANY_TYPE},
        }
        self.has_defaults_params = getfullargspec(has_defaults)
        self.has_defaults_schema = {"x": {"oneOf": ANY_TYPE}}
        self.only_defaults_params = getfullargspec(only_defaults)
        self.only_defaults_schema = {}
        self.typed_params_params = getfullargspec(typed_params)
        self.typed_params_schema = {
            "x": {"oneOf": ANY_TYPE},
            "y": {"type": "integer"},
            "z": {"type": "string"},
        }

    def test_get_no_defaults_schema(self):
        schema = get_no_defaults_schema(self.no_defaults_params)
        assert schema == self.no_defaults_schema

    def test_get_has_defaults_schema(self):
        schema = get_no_defaults_schema(self.has_defaults_params)
        assert schema == self.has_defaults_schema

    def test_get_only_defaults_schema(self):
        schema = get_no_defaults_schema(self.only_defaults_params)
        assert schema == self.only_defaults_schema

    def test_get_typed_params_schema(self):
        schema = get_no_defaults_schema(self.typed_params_params)
        assert schema == self.typed_params_schema


class TestGetDefaultsSchema:
    def setup_method(self):
        def no_defaults(x, y, z):
            return x + y + z

        def has_defaults(x, y=2, z=3):
            return x + y + z

        def only_defaults(x=1, y=2, z=3):
            return x + y + z

        def typed_params(x, y=None, z: str = "test!", d: int = 3):
            return [x, y, z, d]

        self.no_defaults_params = getfullargspec(no_defaults)
        self.no_defaults_schema = {}
        self.has_defaults_params = getfullargspec(has_defaults)
        self.has_defaults_schema = {
            "y": {"oneOf": ANY_TYPE, "default": 2},
            "z": {"oneOf": ANY_TYPE, "default": 3},
        }
        self.only_defaults_params = getfullargspec(only_defaults)
        self.only_defaults_schema = {
            "x": {"oneOf": ANY_TYPE, "default": 1},
            "y": {"oneOf": ANY_TYPE, "default": 2},
            "z": {"oneOf": ANY_TYPE, "default": 3},
        }
        self.typed_params_params = getfullargspec(typed_params)
        self.typed_params_schema = {
            "y": {"oneOf": ANY_TYPE, "default": None},
            "z": {"type": "string", "default": "test!"},
            "d": {"type": "integer", "default": 3},
        }

    def test_get_no_defaults_schema(self):
        schema = get_defaults_schema(self.no_defaults_params)
        assert schema == self.no_defaults_schema

    def test_get_has_defaults_schema(self):
        schema = get_defaults_schema(self.has_defaults_params)
        assert schema == self.has_defaults_schema

    def test_get_only_defaults_schema(self):
        schema = get_defaults_schema(self.only_defaults_params)
        assert schema == self.only_defaults_schema

    def test_get_typed_params_schema(self):
        schema = get_defaults_schema(self.typed_params_params)
        assert schema == self.typed_params_schema
