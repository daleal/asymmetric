"""
A module for every utility of asymmetric.
"""

import inspect
import json
import sys
from typing import Any, Callable, Dict

from starlette.requests import Request
from starlette.responses import JSONResponse


async def generic_call(function: Callable[..., Any], params: Dict[str, Any]) -> Any:
    """
    Executes a function with its params, checking if said function
    is async or not
    """
    if inspect.iscoroutinefunction(function):  # Await async functions
        return await function(**params)
    return function(**params)


def handle_error(error: Exception) -> JSONResponse:
    """Handles errors from the router."""
    return JSONResponse({"message": str(error)}, status_code=500)


def filter_params(function: Callable[..., Any], data: Dict[str, Any]) -> Dict[str, Any]:
    """Filters parameters so that the function recieves only what it needs."""
    # Get the parameters
    params = inspect.getfullargspec(function)
    if params.varkw is not None:
        # The function recieves kwargs, return the full dictionary
        return data
    if not params.args:
        # The function does not recieve args, return an empty dict
        return {}
    # Filter every param whose key is not in the params dictionary
    return {k: v for k, v in data.items() if k in params.args}


async def get_body(request: Request) -> Dict[str, Any]:
    """
    Gets the body of the request and returns an empty dict if the request
    has no body.
    """
    try:
        body = await request.json()
        return body
    except json.decoder.JSONDecodeError:
        return {}


def valid_plain_dict(data: Dict[str, Any], validator: Dict[str, Any]) -> bool:
    """
    Given a data and a validator array, checks if data includes the required
    attributes and if it includes extra attributes.
    """
    possible_attrs = validator.keys()
    required_attrs = filter(lambda k: validator[k]["required"], possible_attrs)
    attrs = data.keys()

    # Check for extra attributes
    if not all(map(lambda x: x in possible_attrs, attrs)):
        return False

    # Check for required attributes
    if not all(map(lambda x: x in attrs, required_attrs)):
        return False

    # Check for invalid types
    if not all(map(lambda k: isinstance(data[k], validator[k]["type"]), attrs)):
        return False

    return True


def terminate_program() -> None:
    """Terminates the server process."""
    sys.exit(1)
