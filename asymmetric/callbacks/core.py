"""
A module for asymmetric's core callback logic.
"""

import httpx
import asyncio
from starlette.responses import JSONResponse

from asymmetric.callbacks.callback_object import CALLBACK_OBJECT_DEFAULTS
from asymmetric.callbacks.utils import valid_callback_data
from asymmetric.constants import HTTP_METHODS
from asymmetric.errors import (
    InvalidCallbackObjectError,
    InvalidCallbackHeadersError
)
from asymmetric.loggers import log
from asymmetric.utils import generic_call, terminate_program


class CallbackClient:

    """
    A class to abstract the callback logic.
    """

    def __init__(self, function, callback):
        self.__function = function
        self.__callback = callback
        self.__headers = {}
        self.__params = {}
        self.__attribute_finders = {}
        self.__invalid_callback_object = False

    @property
    def url(self):
        location = self.__attribute_finders.get("callback_url_header")
        return self.__headers.get(location, None)

    @property
    def http_method(self):
        location = self.__attribute_finders.get("callback_method_header")
        if location not in self.__headers:
            return "POST"  # Default HTTP method
        return self.__headers.get(location).upper()

    @property
    def custom_key(self):
        location = self.__attribute_finders.get("custom_callback_key_header")
        if location in self.__headers:
            return self.__headers.get(location)
        return None

    def handle_callback(self, headers, params):
        """
        Validates that the callback data from the request is correct
        and delegates the main function call. Returns a JSON response.
        """
        if self.__invalid_callback_object:
            # Callback object was defective, server should have stopped
            return JSONResponse(
                {"message": self.__invalid_callback_object},
                status_code=500
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

            return JSONResponse({}, status_code=200)
        except InvalidCallbackHeadersError as error:
            return JSONResponse({"message": str(error)}, status_code=422)

    def prepare_and_validate_finders(self):
        """
        Collects the callback data finders and validates
        that they are correct on decoration-time.
        """
        try:
            self.__validate_callback_json_data()
            self.__get_header_finders()
        except InvalidCallbackObjectError as err:
            self.__invalid_callback_object = str(err)
            log(str(error), info="warn")
            terminate_program()

    def __validate_callback_json_data(self):
        """
        Validates that the callback dictionary is a valid callback
        dictionary or raises an error.
        """
        if not valid_callback_data(self.__callback):
            raise InvalidCallbackObjectError("Invalid callback object")

    def __get_header_finders(self):
        """
        Gets the header attribute finders to search for some data
        on every request header on decoration-time.
        """
        if isinstance(self.__callback, bool):
            # Callback attribute is True
            self.__attribute_finders = CALLBACK_OBJECT_DEFAULTS
        else:
            # Callback attribute is an object, get callback attribute finders
            for attr, default_value in CALLBACK_OBJECT_DEFAULTS.items():
                if attr in self.__callback:
                    self.__attribute_finders[attr] = self.__callback[attr]
                else:
                    self.__attribute_finders[attr] = default_value

    def __validate_callback_url(self):
        """
        Validates that the callback URL within the request
        header is valid.
        """
        if self.url is None:
            raise InvalidCallbackHeadersError("Invalid callback URL")

    def __validate_callback_http_method(self):
        """
        Validates that the callback HTTP method within the request
        header is valid.
        """
        if self.http_method.lower() not in HTTP_METHODS:
            raise InvalidCallbackHeadersError("Invalid callback HTTP method")

    async def __callback_call(self):
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
