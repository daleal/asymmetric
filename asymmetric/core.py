"""
The main module of asymmetric.
"""

import asyncio
from starlette.applications import Starlette
from starlette.responses import JSONResponse

from asymmetric.callbacks.core import CallbackClient
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
    terminate_program,
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
        Intercept all attribute/method calls to the assymetric object
        if they aren't part of it and redirect them to the Starlette app.
        """
        return getattr(self.__app, attr)

    def router(
            self,
            route,
            methods=["post"],
            response_code=200,
            callback=False
    ):
        """
        Method to use for decorating the function wanting to be transformed
        to an API.
        """
        methods = [
            http_verb(x) for x in methods if http_verb(x) in HTTP_METHODS
        ]

        def decorator(function):
            """
            Function decorator. Receives the main function and wraps it as a
            starlette endpoint. Returns the original unwrapped function.
            """

            if callback:
                callback_client = CallbackClient(function, callback)
                callback_client.prepare_and_validate_finders()

            @self.__app.route(route, methods=methods)
            async def wrapper(request):
                asyncio.ensure_future(
                    log_request(request, route, function))

                try:
                    # Get the body
                    body = await get_body(request)

                    # Get params and headers
                    params = filter_params(function, body)
                    headers = request.headers

                    if not callback:
                        # Process and return the result
                        return JSONResponse(
                            await generic_call(function, params),
                            status_code=response_code
                        )

                    return callback_client.handle_callback(headers, params)
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
                terminate_program()  # TODO: exit the server correctly

            return function
        return decorator


asymmetric_object = Asymmetric()
