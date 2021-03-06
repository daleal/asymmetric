import json
from inspect import getfullargspec

from asymmetric.callbacks.callback_object import (
    CALLBACK_OBJECT_DEFAULTS,
    CALLBACK_OBJECT_METADATA,
)
from asymmetric.endpoints import Endpoint
from asymmetric.openapi.constants import ANY_TYPE
from asymmetric.openapi.core import (
    get_defaults_schema,
    get_no_defaults_schema,
    get_openapi_components,
    get_openapi_endpoint_body_schema,
    get_openapi_endpoint_headers_schema,
    get_openapi_endpoint_responses_schema,
    get_openapi_endpoint_schema,
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
        self.typed_params = getfullargspec(typed_params)
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
        schema = get_defaults_schema(self.typed_params)
        assert schema == self.typed_params_schema


class TestGetOpenAPIBodySchema:
    def setup_method(self):
        def no_defaults(x, y, z):
            return x + y + z

        def has_defaults(x, y=2, z=3):
            return x + y + z

        def only_defaults(x=1, y=2, z=3):
            return x + y + z

        def typed_params(x, y, z=None, a: str = "test!", b: int = 3):
            return [x, y, z, a, b]

        def kwargs_params(x, y: str, z: int = 3, **kwargs):
            return [x, y, z, kwargs]

        def decorator(function):
            def wrapper():
                print("wrapping...")
                function()
                print("unwrapping...")

            return wrapper

        def create_endpoint(function):
            return Endpoint(
                "/v1/test/open/api",
                "GET",
                function,
                decorator(function),
            )

        self.no_defaults_endpoint = create_endpoint(no_defaults)
        self.no_defaults_schema = {
            "type": "object",
            "properties": {
                "x": {"oneOf": ANY_TYPE},
                "y": {"oneOf": ANY_TYPE},
                "z": {"oneOf": ANY_TYPE},
            },
            "additionalProperties": False,
        }
        self.has_defaults_endpoint = create_endpoint(has_defaults)
        self.has_defaults_schema = {
            "type": "object",
            "properties": {
                "x": {"oneOf": ANY_TYPE},
                "y": {"oneOf": ANY_TYPE, "default": 2},
                "z": {"oneOf": ANY_TYPE, "default": 3},
            },
            "additionalProperties": False,
        }
        self.only_defaults_endpoint = create_endpoint(only_defaults)
        self.only_defaults_schema = {
            "type": "object",
            "properties": {
                "x": {"oneOf": ANY_TYPE, "default": 1},
                "y": {"oneOf": ANY_TYPE, "default": 2},
                "z": {"oneOf": ANY_TYPE, "default": 3},
            },
            "additionalProperties": False,
        }
        self.typed_endpoint = create_endpoint(typed_params)
        self.typed_schema = {
            "type": "object",
            "properties": {
                "x": {"oneOf": ANY_TYPE},
                "y": {"oneOf": ANY_TYPE},
                "z": {"oneOf": ANY_TYPE, "default": None},
                "a": {"type": "string", "default": "test!"},
                "b": {"type": "integer", "default": 3},
            },
            "additionalProperties": False,
        }
        self.kwargs_endpoint = create_endpoint(kwargs_params)
        self.kwargs_schema = {
            "type": "object",
            "properties": {
                "x": {"oneOf": ANY_TYPE},
                "y": {"type": "string"},
                "z": {"type": "integer", "default": 3},
            },
            "additionalProperties": True,
        }

    def test_no_defaults_endpoint(self):
        schema = get_openapi_endpoint_body_schema(self.no_defaults_endpoint)
        assert schema == self.no_defaults_schema

    def test_has_defaults_endpoint(self):
        schema = get_openapi_endpoint_body_schema(self.has_defaults_endpoint)
        assert schema == self.has_defaults_schema

    def test_only_defaults_endpoint(self):
        schema = get_openapi_endpoint_body_schema(self.only_defaults_endpoint)
        assert schema == self.only_defaults_schema

    def test_typed_endpoint(self):
        schema = get_openapi_endpoint_body_schema(self.typed_endpoint)
        assert schema == self.typed_schema

    def test_kwargs_endpoint(self):
        schema = get_openapi_endpoint_body_schema(self.kwargs_endpoint)
        assert schema == self.kwargs_schema


class TestGetOpenAPIEndpointHeadersSchema:
    def setup_method(self):
        def function(x):
            return x

        def decorator(function):
            def wrapper():
                print("wrapping...")
                function()
                print("unwrapping...")

            return wrapper

        def create_endpoint(callback):
            return Endpoint(
                "/v1/test/open/api",
                "GET",
                function,
                decorator(function),
                callback=callback,
            )

        self.no_callback_endpoint = create_endpoint(False)
        self.callback_endpoint = create_endpoint(True)

    def test_no_callback_endpoint_headers_schema(self):
        schema = get_openapi_endpoint_headers_schema(self.no_callback_endpoint)
        assert schema == []

    def test_callback_endpoint_headers_schema(self):
        schema = get_openapi_endpoint_headers_schema(self.callback_endpoint)
        assert schema == [
            {
                "in": "header",
                "name": header,
                "schema": {
                    "type": "string",
                },
                "required": CALLBACK_OBJECT_METADATA[key]["required"],
                "description": CALLBACK_OBJECT_METADATA[key]["description"],
            }
            for key, header in CALLBACK_OBJECT_DEFAULTS.items()
        ]


class TestGetOpenAPIEndpointResponsesSchema:
    def setup_method(self):
        def no_response_annotation(x):
            return x

        def response_annotation(x) -> int:
            return int(x)

        def decorator(function):
            def wrapper():
                print("wrapping...")
                function()
                print("unwrapping...")

            return wrapper

        def create_endpoint(function, callback):
            return Endpoint(
                "/v1/test/open/api",
                "GET",
                function,
                decorator(function),
                callback=callback,
                response_code=200,
            )

        self.not_annotated_no_callback_endpoint = create_endpoint(
            no_response_annotation,
            False,
        )
        self.not_annotated_no_callback_schema = {
            "200": {
                "$ref": "#/components/responses/SuccesfulOperation",
            },
            "500": {
                "$ref": "#/components/responses/InternalError",
            },
        }
        self.annotated_no_callback_endpoint = create_endpoint(
            response_annotation,
            False,
        )
        self.annotated_no_callback_schema = {
            "200": {
                "$ref": "#/components/responses/SuccesfulOperation",
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "integer",
                        },
                    },
                },
            },
            "500": {
                "$ref": "#/components/responses/InternalError",
            },
        }
        self.not_annotated_callback_endpoint = create_endpoint(
            no_response_annotation,
            True,
        )
        self.not_annotated_callback_schema = {
            "202": {
                "$ref": "#/components/responses/AcceptedOperation",
            },
            "500": {
                "$ref": "#/components/responses/InternalError",
            },
        }
        self.annotated_callback_endpoint = create_endpoint(
            response_annotation,
            True,
        )
        self.annotated_callback_schema = {
            "202": {
                "$ref": "#/components/responses/AcceptedOperation",
            },
            "500": {
                "$ref": "#/components/responses/InternalError",
            },
        }

    def test_not_annotated_no_callback_endpoint(self):
        schema = get_openapi_endpoint_responses_schema(
            self.not_annotated_no_callback_endpoint
        )
        assert schema == self.not_annotated_no_callback_schema

    def test_annotated_no_callback_endpoint(self):
        schema = get_openapi_endpoint_responses_schema(
            self.annotated_no_callback_endpoint
        )
        assert schema == self.annotated_no_callback_schema

    def test_not_annotated_callback_endpoint(self):
        schema = get_openapi_endpoint_responses_schema(
            self.not_annotated_callback_endpoint
        )
        assert schema == self.not_annotated_callback_schema

    def test_annotated_callback_endpoint(self):
        schema = get_openapi_endpoint_responses_schema(self.annotated_callback_endpoint)
        assert schema == self.annotated_callback_schema


class TestGetOpenAPIEndpointSchema:
    def setup_method(self):
        def get_function():
            return "This is a test!"

        def post_function(x, y):
            """POST-it!"""
            return x + y

        def decorator(function):
            def wrapper():
                print("wrapping...")
                function()
                print("unwrapping...")

            return wrapper

        def create_endpoint(function, method, callback):
            return Endpoint(
                "/v1/test/open/api",
                "GET",
                function,
                decorator(function),
                callback=callback,
            )

        self.no_callback_endpoints = {
            "get": create_endpoint(get_function, "get", False),
            "post": create_endpoint(post_function, "post", False),
        }
        self.callback_endpoints = {
            "get": create_endpoint(get_function, "get", True),
            "post": create_endpoint(post_function, "post", True),
        }

    def test_no_callback_schema_generation(self):
        schema = get_openapi_endpoint_schema(self.no_callback_endpoints)
        assert schema == {
            "get": {
                "description": "No description provided.",
                "parameters": [],
                "responses": {
                    "200": {
                        "$ref": "#/components/responses/SuccesfulOperation",
                    },
                    "500": {
                        "$ref": "#/components/responses/InternalError",
                    },
                },
            },
            "post": {
                "description": "POST-it!",
                "parameters": [],
                "responses": {
                    "200": {
                        "$ref": "#/components/responses/SuccesfulOperation",
                    },
                    "500": {
                        "$ref": "#/components/responses/InternalError",
                    },
                },
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "x": {"oneOf": ANY_TYPE},
                                    "y": {"oneOf": ANY_TYPE},
                                },
                                "additionalProperties": False,
                            },
                        },
                    },
                },
            },
        }

    def test_callback_schema_generation(self):
        schema = get_openapi_endpoint_schema(self.callback_endpoints)
        assert schema == {
            "get": {
                "description": "No description provided.",
                "parameters": [
                    {
                        "in": "header",
                        "name": header,
                        "schema": {
                            "type": "string",
                        },
                        "required": CALLBACK_OBJECT_METADATA[key]["required"],
                        "description": CALLBACK_OBJECT_METADATA[key]["description"],
                    }
                    for key, header in CALLBACK_OBJECT_DEFAULTS.items()
                ],
                "responses": {
                    "202": {
                        "$ref": "#/components/responses/AcceptedOperation",
                    },
                    "500": {
                        "$ref": "#/components/responses/InternalError",
                    },
                },
            },
            "post": {
                "description": "POST-it!",
                "parameters": [
                    {
                        "in": "header",
                        "name": header,
                        "schema": {
                            "type": "string",
                        },
                        "required": CALLBACK_OBJECT_METADATA[key]["required"],
                        "description": CALLBACK_OBJECT_METADATA[key]["description"],
                    }
                    for key, header in CALLBACK_OBJECT_DEFAULTS.items()
                ],
                "responses": {
                    "202": {
                        "$ref": "#/components/responses/AcceptedOperation",
                    },
                    "500": {
                        "$ref": "#/components/responses/InternalError",
                    },
                },
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "x": {"oneOf": ANY_TYPE},
                                    "y": {"oneOf": ANY_TYPE},
                                },
                                "additionalProperties": False,
                            },
                        },
                    },
                },
            },
        }


class TestGetOpenAPIComponents:
    def test_get_openapi_components(self):
        components = get_openapi_components()
        assert "responses" in components
        assert "SuccesfulOperation" in components["responses"]
        assert "AcceptedOperation" in components["responses"]
        assert "InternalError" in components["responses"]
