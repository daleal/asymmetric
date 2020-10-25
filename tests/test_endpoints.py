import pytest

from asymmetric.endpoints import Endpoint, Endpoints
from asymmetric.errors import DuplicatedEndpointError


class TestEndpointClass:
    def setup_method(self):
        def function(x, y):
            return x + y

        def docstring_function(x, y):
            """This is a test docstring!"""
            return x + y

        def decorator(function):
            def wrapper(*args, **kwargs):
                return function(*args, **kwargs) + 10

            return wrapper

        self.route = "/v1/test/endpoint/class"
        self.method = "POST"
        self.response_code = 200
        self.function = function
        self.decorated_function = decorator(function)
        self.docstring_function = docstring_function
        self.decorated_docstring_function = decorator(docstring_function)

    def test_endpoint_instance_creation(self):
        instance = Endpoint(
            self.route,
            self.method,
            self.function,
            self.decorated_function,
            response_code=self.response_code,
        )

        assert isinstance(instance, Endpoint) is True
        assert instance.route == self.route
        assert instance.method == self.method
        assert instance.function == self.function
        assert instance.docstring == "No description provided."
        assert instance.callback is False
        assert instance.response_code == self.response_code

    def test_docstring_endpoint_function(self):
        instance = Endpoint(
            self.route,
            self.method,
            self.docstring_function,
            self.decorated_docstring_function,
        )

        assert instance.docstring == "This is a test docstring!"

    def test_endpoint_callback_response_code(self):
        instance = Endpoint(
            self.route,
            self.method,
            self.function,
            self.decorated_function,
            callback=True,
            response_code=self.response_code,
        )
        assert instance.callback is True
        assert instance.response_code != self.response_code
        assert instance.response_code == 202


class TestEndpointsClass:
    def setup_method(self):
        def function(x, y):
            return x + y

        def decorator(function):
            def wrapper(*args, **kwargs):
                return function(*args, **kwargs) + 10

            return wrapper

        self.endpoints = Endpoints()

        self.route = "/v1/test/endpoint/class"
        self.methods = ["GET", "POST", "PATCH"]
        self.function = function
        self.decorated_function = decorator(function)

    def test_create_route(self):
        created_route = self.endpoints._Endpoints__create_route(self.route)
        assert created_route == {}
        assert self.route in self.endpoints._Endpoints__endpoints

    def test_get_route(self):
        assert self.endpoints._Endpoints__get_route(self.route) is None
        self.endpoints._Endpoints__create_route(self.route)
        assert self.endpoints._Endpoints__get_route(self.route) == {}

    def test_get_empty_endpoint(self):
        endpoint = self.endpoints._Endpoints__get_endpoint(self.route, self.methods[0])
        assert endpoint is None

    def test_get_route_only_endpoint(self):
        self.endpoints._Endpoints__create_route(self.route)
        assert self.endpoints._Endpoints__get_route(self.route) == {}
        endpoint = self.endpoints._Endpoints__get_endpoint(self.route, self.methods[0])
        assert endpoint is None

    def test_get_complete_endpoint(self):
        self.endpoints._Endpoints__create_route(self.route)
        route = self.endpoints._Endpoints__get_route(self.route)
        assert route == {}

        endpoint_object = Endpoint(
            self.route,
            self.methods[0],
            self.function,
            self.decorated_function,
        )

        route[self.methods[0]] = endpoint_object

        endpoint = self.endpoints._Endpoints__get_endpoint(self.route, self.methods[0])
        assert isinstance(endpoint, Endpoint)

    def test_add_one_endpoint(self):
        self.endpoints._Endpoints__add_endpoint(
            self.route,
            self.methods[0],
            self.function,
            self.decorated_function,
        )

        created = self.endpoints._Endpoints__endpoints[self.route][self.methods[0]]
        assert isinstance(created, Endpoint) is True
        assert created in self.endpoints.endpoints[self.route].values()

    def test_add_endpoint_two_different_elements(self):
        self.endpoints._Endpoints__add_endpoint(
            self.route,
            self.methods[0],
            self.function,
            self.decorated_function,
        )

        self.endpoints._Endpoints__add_endpoint(
            self.route,
            self.methods[1],
            self.function,
            self.decorated_function,
        )

        first = self.endpoints._Endpoints__endpoints[self.route][self.methods[0]]
        second = self.endpoints._Endpoints__endpoints[self.route][self.methods[1]]

        assert isinstance(first, Endpoint) is True
        assert isinstance(second, Endpoint) is True

    def test_add_endpoint_duplicated(self):
        with pytest.raises(DuplicatedEndpointError):
            self.endpoints._Endpoints__add_endpoint(
                self.route,
                self.methods[0],
                self.function,
                self.decorated_function,
            )

            self.endpoints._Endpoints__add_endpoint(
                self.route,
                self.methods[0],
                self.function,
                self.decorated_function,
            )

    def test_add_endpoints(self):
        self.endpoints.add_endpoints(
            self.route,
            self.methods,
            self.function,
            self.decorated_function,
        )

        first = self.endpoints._Endpoints__endpoints[self.route][self.methods[0]]
        second = self.endpoints._Endpoints__endpoints[self.route][self.methods[1]]
        third = self.endpoints._Endpoints__endpoints[self.route][self.methods[2]]

        assert isinstance(first, Endpoint) is True
        assert isinstance(second, Endpoint) is True
        assert isinstance(third, Endpoint) is True
