"""
A module for containing the endpoint logic of asymmetric.
"""

from inspect import getdoc
from typing import Any, Callable, Dict, List, Optional, Union

from asymmetric.errors import DuplicatedEndpointError


class Endpoint:

    """
    Class to encapsulate an endpoint.
    """

    def __init__(
        self,
        route: str,
        method: str,
        function: Callable[..., Any],
        decorated_function: Callable[..., Any],
        callback: Union[Dict[str, Any], bool] = False,
        response_code: int = 200,
    ) -> None:
        self.__route: str = route
        self.__method: str = method
        self.__function: Callable[..., Any] = function
        self.__decorated_function: Callable[..., Any] = decorated_function
        self.__callback = callback
        self.__response_code: int = response_code

    @property
    def route(self) -> str:
        """Returns the route of the endpoint."""
        return self.__route

    @property
    def method(self) -> str:
        """Returns the HTTP method of the endpoint."""
        return self.__method

    @property
    def response_code(self) -> int:
        """Returns the response code of the endpoint on a request."""
        return self.__response_code if not self.__callback else 202

    @property
    def callback(self) -> Union[Dict[str, Any], bool]:
        """Returns the response code of the endpoint on a request."""
        return self.__callback

    @property
    def function(self) -> Callable[..., Any]:
        """Returns the raw function of the endpoint."""
        return self.__function

    @property
    def docstring(self) -> str:
        """Returns the docstring content of the endpoint function."""
        docstring = getdoc(self.__function)
        return docstring or "No description provided."


class Endpoints:  # pylint: disable=R0903

    """
    Class to encapsulate the endpoints logic.
    """

    def __init__(self) -> None:
        self.__endpoints: Dict[str, Dict[str, Endpoint]] = {}

    @property
    def endpoints(self) -> Dict[str, Dict[str, Endpoint]]:
        """Returns the endpoints dict."""
        return self.__endpoints

    def add_endpoints(
        self,
        route: str,
        methods: List[str],
        function: Callable[..., Any],
        decorated_function: Callable[..., Any],
        callback: Union[Dict[str, Any], bool] = False,
        response_code: int = 200,
    ) -> None:
        """
        Adds an endpoint for every method specified.
        """
        for method in methods:
            self.__add_endpoint(
                route,
                method,
                function,
                decorated_function,
                callback=callback,
                response_code=response_code,
            )

    def __add_endpoint(
        self,
        route: str,
        method: str,
        function: Callable[..., Any],
        decorated_function: Callable[..., Any],
        callback: Union[Dict[str, Any], bool] = False,
        response_code: int = 200,
    ) -> None:
        """
        Checks if the desired endpoint does not exist. If it exists,
        it raises an error. Otherwise, it creates the endpoint
        and stores it.
        """
        if self.__get_endpoint(route, method) is not None:
            message = f"Endpoint '{route}' with HTTP method '{method.upper()}' "
            message += "was defined twice."
            raise DuplicatedEndpointError(message)

        endpoint = Endpoint(
            route,
            method,
            function,
            decorated_function,
            callback=callback,
            response_code=response_code,
        )

        route_dictionary = self.__get_route(route)
        if route_dictionary is None:
            route_dictionary = self.__create_route(route)
        route_dictionary[method] = endpoint

    def __get_route(self, route: str) -> Optional[Dict[str, Endpoint]]:
        """
        Returns the route dictionary containing each method
        as a key. If the route has not been used, returns None.
        """
        if route not in self.__endpoints:
            return None
        return self.__endpoints[route]

    def __create_route(self, route: str) -> Dict[str, Endpoint]:
        """Creates a route and returns it."""
        self.__endpoints[route] = {}
        return self.__endpoints[route]

    def __get_endpoint(self, route: str, method: str) -> Optional[Endpoint]:
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
