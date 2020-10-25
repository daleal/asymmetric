"""
A module for asymmetric's core callback logic.
"""

import asyncio
from typing import Any, Callable, Dict, Optional, Union

import httpx
from starlette.datastructures import Headers
from starlette.responses import JSONResponse

from asymmetric.callbacks.utils import get_header_finders, validate_callback_data
from asymmetric.constants import HTTP_METHODS
from asymmetric.errors import InvalidCallbackHeadersError, InvalidCallbackObjectError
from asymmetric.loggers import log
from asymmetric.utils import generic_call


class CallbackClient:

    """
    A class to abstract the callback logic.
    """

    def __init__(
        self, function: Callable[..., Any], callback: Union[Dict[str, Any], bool]
    ) -> None:
        self.__function = function
        self.__attribute_finders = self.__prepare_and_validate_finders(callback)
        self.__headers = Headers()
        self.__params: Dict[str, str] = {}
        self.__invalid_callback_object = ""

    @property
    def url(self) -> str:
        """Returns the callback URL if it was included, or None."""
        location = self.__attribute_finders.get("callback_url_header")
        return self.__headers.get(location, "") if location is not None else ""

    @property
    def http_method(self) -> str:
        """Returns the callback HTTP method if it was included, or POST."""
        location = self.__attribute_finders.get("callback_method_header", "")
        # POST is the default HTTP method
        http_method = self.__headers[location] if location in self.__headers else "POST"
        return http_method.upper()

    @property
    def custom_key(self) -> Optional[str]:
        """Returns the custom callback key container if it was included, or None."""
        location = self.__attribute_finders.get("custom_callback_key_header", "")
        if location in self.__headers:
            return self.__headers.get(location)
        return None

    def handle_callback(self, headers: Headers, params: Dict[str, Any]) -> JSONResponse:
        """
        Validates that the callback data from the request is correct
        and delegates the main function call. Returns a JSON response.
        """
        if self.__invalid_callback_object:
            # Callback object was defective, server should have stopped
            return JSONResponse(
                {"message": self.__invalid_callback_object}, status_code=500
            )

        try:
            # Set headers and params
            self.__headers = headers
            self.__params = params

            # Validate callback data
            self.__validate_callback_url()
            self.__validate_callback_http_method()

            # Delegate function
            asyncio.ensure_future(self.__callback_call())

            return JSONResponse({}, status_code=202)
        except InvalidCallbackHeadersError as error:
            return JSONResponse({"message": str(error)}, status_code=422)

    @staticmethod
    def __prepare_and_validate_finders(
        callback: Union[Dict[str, Any], bool]
    ) -> Dict[str, str]:
        """
        Collects and returns the callback data finders and validates
        that they are correct on decoration-time.
        """
        try:
            validate_callback_data(callback)
            return get_header_finders(callback)
        except InvalidCallbackObjectError as error:
            log(str(error), level="critical")
            raise InvalidCallbackObjectError(error) from error

    def __validate_callback_url(self) -> None:
        """
        Validates that the callback URL within the request
        header is valid.
        """
        if not self.url:
            raise InvalidCallbackHeadersError("Invalid callback URL")

    def __validate_callback_http_method(self) -> None:
        """
        Validates that the callback HTTP method within the request
        header is valid.
        """
        if self.http_method.lower() not in HTTP_METHODS:
            raise InvalidCallbackHeadersError("Invalid callback HTTP method")

    async def __callback_call(self) -> None:
        """
        Executes the function and makes the request to the callback endpoint.
        """
        try:
            response = await generic_call(self.__function, self.__params)
            if self.custom_key is not None:
                response = {self.custom_key: response}

            async with httpx.AsyncClient() as client:
                await client.request(
                    self.http_method,
                    self.url,
                    json=response,
                )
        except Exception as error:
            message = "Error while executing the delegated method: "
            message += str(error)
            log(message, level="warn")
