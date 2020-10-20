"""
A module for every utility of asymmetric.
"""

import inspect
import json
from starlette.responses import JSONResponse


async def generic_call(function, params):
    """
    Executes a function with its params, checking if said function
    is async or not
    """
    if inspect.iscoroutinefunction(function):  # Await async functions
        return await function(**params)
    return function(**params)


def handle_error(error):
    """Handles errors from the router."""
    if isinstance(error, AssertionError):
        return JSONResponse({})
    else:
        return JSONResponse(
            {"message": str(error)},
            status_code=500
        )


def filter_params(function, data):
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


async def get_body(request):
    """
    Gets the body of the request and returns an empty dict if the request
    has no body.
    """
    try:
        body = await request.json()
        return body
    except json.decoder.JSONDecodeError:
        return {}
