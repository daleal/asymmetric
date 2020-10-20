"""
The main module of asymmetric.
"""

import sys
import asyncio
from starlette.applications import Starlette
from starlette.responses import JSONResponse

from asymmetric.constants import HTTP_METHODS
from asymmetric.endpoints import Endpoints
from asymmetric.errors import DuplicatedEndpointError
from asymmetric.helpers import http_verb
from asymmetric.loggers import log, log_request
from asymmetric.utils import (
    generic_call,
    handle_error,
    filter_params,
    get_body,
)


class Asymmetric:

    """
    Main class to encapsulate every important feature of
    the asymmetric package.
    """

    def __init__(self):
        self.__app = Starlette()
        self.__endpoints = Endpoints()

    async def __call__(self, scope, receive, send):
        return await self.__app.__call__(scope, receive, send)

    def __getattr__(self, attr):
        """
        Intercept all attribute/method calls to  of things
        that aren't within the object.
        """
        return getattr(self.__app, attr)

    def router(self, route, methods=["post"], response_code=200):
        """
        Method to use for decorating the function wanting to be transformed
        to an API.
        """
        methods = [
            http_verb(x) for x in methods if http_verb(x) in HTTP_METHODS
        ]

        def decorator(function):
            """
            Function decorator. Recieves the main function and wraps it as a
            starlette endpoint. Returns the original unwrapped function.
            """
            @self.__app.route(route, methods=methods)
            async def wrapper(request):
                try:
                    asyncio.ensure_future(
                        log_request(request, route, function))

                    # Get the body
                    body = await get_body(request)

                    params = filter_params(function, body)
                    return JSONResponse(
                        await generic_call(function, params),
                        status_code=response_code
                    )
                except Exception as error:
                    return handle_error(error)

            # Save Endpoint
            try:
                self.__endpoints.add_endpoints(
                    route,
                    methods,
                    response_code,
                    function,  # Save unchanged function
                    wrapper,   # Save starlette decorated function
                )
            except DuplicatedEndpointError as err:
                log(f"DuplicatedRouteError: {err}", level="error")
                sys.exit(1)  # TODO: exit the server correctly

            return function
        return decorator


asymmetric_object = Asymmetric()
