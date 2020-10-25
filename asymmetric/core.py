"""
The main module of asymmetric.
"""

import asyncio
from typing import Any, Callable, Dict, List, Union

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse
from starlette.types import Receive, Scope, Send

from asymmetric.callbacks.core import CallbackClient
from asymmetric.constants import (
    HTTP_METHODS,
    OPENAPI_SPEC_ROUTE,
    REDOC_DOCUMENTATION_ROUTE,
    SWAGGER_DOCUMENTATION_ROUTE,
)
from asymmetric.endpoints import Endpoints
from asymmetric.errors import DuplicatedEndpointError
from asymmetric.helpers import http_verb
from asymmetric.loggers import log, log_request
from asymmetric.openapi.documentation_renderers import get_redoc_html, get_swagger_html
from asymmetric.openapi.utils import get_openapi
from asymmetric.singleton import AsymmetricSingleton
from asymmetric.utils import filter_params, generic_call, get_body, handle_error


class _Asymmetric(metaclass=AsymmetricSingleton):

    """
    Main class to encapsulate every important feature of
    the asymmetric package.
    """

    def __init__(self) -> None:
        self.__app: Starlette = Starlette()
        self.__endpoints: Endpoints = Endpoints()
        self.__openapi_schema: Union[Dict[str, Any], None] = None
        self.__setup()

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        await self.__app.__call__(scope, receive, send)

    def __getattr__(self, attr: Any) -> Any:
        """
        Intercept all attribute/method calls to the assymetric object
        if they aren't part of it and redirect them to the Starlette app.
        """
        return getattr(self.__app, attr)

    @property
    def openapi(self) -> Dict[str, Any]:
        """
        Returns the openapi schema. If it does not exist, it creates it
        and returns it.
        """
        if self.__openapi_schema is None:
            self.__openapi_schema = get_openapi(self, "Asymmetric API")
        return self.__openapi_schema

    def __setup(self) -> None:
        """Sets up the API."""
        # Set up the endpoint for the openapi json schema
        # pylint: disable=W0612
        @self.__app.route(OPENAPI_SPEC_ROUTE)
        def openapi_schema(request: Request) -> JSONResponse:
            return JSONResponse(self.openapi)

        # Set up the endpoint for the Swagger interactive documentation
        # pylint: disable=W0612
        @self.__app.route(SWAGGER_DOCUMENTATION_ROUTE)
        def swagger(request: Request) -> HTMLResponse:
            return HTMLResponse(get_swagger_html("Asymmetric API"))

        # Set up the endpoint for the ReDoc interactive documentation
        # pylint: disable=W0612
        @self.__app.route(REDOC_DOCUMENTATION_ROUTE)
        def redoc(request: Request) -> HTMLResponse:
            return HTMLResponse(get_redoc_html("Asymmetric API"))

    def router(
        self,
        route: str,
        methods: List[str] = ["post"],
        response_code: int = 200,
        callback: Union[Dict[str, Any], bool] = False,
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """
        Method to use for decorating the function wanting to be transformed
        to an API.
        """
        methods = [http_verb(x) for x in methods if http_verb(x) in HTTP_METHODS]

        def decorator(function: Callable[..., Any]) -> Callable[..., Any]:
            """
            Function decorator. Receives the main function and wraps it as a
            starlette endpoint. Returns the original unwrapped function.
            """

            if callback:
                callback_client = CallbackClient(function, callback)

            @self.__app.route(route, methods=methods)
            async def wrapper(request: Request) -> JSONResponse:
                asyncio.ensure_future(log_request(request, route, function))

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
                            status_code=response_code,
                        )

                    return callback_client.handle_callback(headers, params)
                except Exception as error:
                    return handle_error(error)

            # Save Endpoint
            try:
                self.__endpoints.add_endpoints(
                    route,
                    methods,
                    function,  # Save unchanged function
                    wrapper,  # Save starlette decorated function
                    callback=callback,
                    response_code=response_code,
                )
            except DuplicatedEndpointError as error:
                log(f"DuplicatedEndpointError: {error}", level="critical")
                raise DuplicatedEndpointError(error) from error

            return function

        return decorator


asymmetric_object = _Asymmetric()
