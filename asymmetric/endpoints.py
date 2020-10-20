"""
A module for containing the endpoint logic of asymmetric.
"""

from asymmetric.errors import DuplicatedEndpointError


class Endpoints:

    """
    Class to encapsulate the endpoints logic.
    """

    def __init__(self):
        self.__endpoints = {}

    def add_endpoints(
            self,
            route,
            methods,
            response_code,
            function,
            decorated_function,
    ):
        """
        Adds an endpoint for every method specified.
        """
        for method in methods:
            self.__add_endpoint(
                route,
                method,
                response_code,
                function,
                decorated_function,
            )

    def __add_endpoint(
            self,
            route,
            method,
            response_code,
            function,
            decorated_function,
    ):
        """
        Checks if the desired endpoint does not exist. If it exists,
        it raises an error. Otherwise, it creates the endpoint
        and stores it.
        """
        if self.__get_endpoint(route, method) is not None:
            message = f"Endpoint '{route}' with HTTP method '{method}' "
            message += "was defined twice."
            raise DuplicatedEndpointError(message)

        endpoint = Endpoint(
            route,
            method,
            response_code,
            function,
            decorated_function,
        )

        if self.__get_route(route) is None:
            self.__create_route(route)
        self.__get_route(route)[method] = endpoint

    def __get_route(self, route):
        """
        Returns the route dictionary containing each method
        as a key. If the route has not been used, returns None.
        """
        if route not in self.__endpoints:
            return None
        return self.__endpoints[route]

    def __create_route(self, route):
        """Creates a route."""
        self.__endpoints[route] = {}

    def __get_endpoint(self, route, method):
        """
        Returns the endpoint object for a specific route/method
        combination. If said combination does not exist, returns None.
        """
        route_data = self.__get_route(route)
        if route_data is None:
            return None
        if method not in route_data:
            return None
        return route_data[method]


class Endpoint:

    """
    Class to encapsulate an endpoint.
    """

    def __init__(
            self,
            route,
            method,
            response_code,
            function,
            decorated_function,
    ):
        self.__route = route
        self.__method = method
        self.__response_code = response_code
        self.__function = function
        self.__decorated_function = decorated_function

    @property
    def route(self):
        """Returns the route of the endpoint."""
        return self.__route

    @property
    def method(self):
        """Returns the HTTP method of the endpoint."""
        return self.__method

    @property
    def response_code(self):
        """Returns the response code of the endpoint."""
        return self.__response_code

    @property
    def function(self):
        """Returns the raw function of the endpoint."""
        return self.__function
