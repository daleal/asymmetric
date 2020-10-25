"""
Module to hold the openapi documentation creation utilities.
"""

import functools
from inspect import FullArgSpec, getfullargspec
from typing import Any, Dict

from asymmetric.endpoints import Endpoint
from asymmetric.openapi.constants import ANY_TYPE
from asymmetric.openapi.helpers import type_to_string


def get_parameters_amount(params: FullArgSpec) -> Dict[str, int]:
    """
    Gets a params object retrieved from a function with getfullargspec and returns
    a dictionary with the amount of default and not default arguments.
    """
    parameters_amount = len(params.args)
    defaults_amount = 0 if params.defaults is None else len(params.defaults)
    no_defaults_amount = parameters_amount - defaults_amount
    return {"no_defaults": no_defaults_amount, "defaults": defaults_amount}


def get_no_defaults_schema(params: FullArgSpec) -> Dict[str, Any]:
    """Gets the parameters without a default option of the method's params."""
    no_defaults = get_parameters_amount(params)["no_defaults"]
    schema: Dict[str, Any] = {}
    for index in range(no_defaults):
        param = params.args[index]
        param_label = "type" if param in params.annotations else "oneOf"
        param_type: Any = (
            type_to_string(params.annotations[param])
            if param in params.annotations
            else ANY_TYPE
        )
        schema[param] = {param_label: param_type}
    return schema


def get_defaults_schema(params: FullArgSpec) -> Dict[str, Any]:
    """Gets the parameters with a default option of the method's params."""
    params_amount = get_parameters_amount(params)
    defaults = params_amount["defaults"]
    offset = params_amount["no_defaults"]
    schema: Dict[str, Any] = {}
    for index in range(defaults):
        param = params.args[offset + index]
        default_value = params.defaults[index]  # type: ignore
        param_label = "type" if param in params.annotations else "oneOf"
        param_type: Any = (
            type_to_string(params.annotations[param])
            if param in params.annotations
            else ANY_TYPE
        )
        schema[param] = {param_label: param_type, "default": default_value}
    return schema


def get_openapi_endpoint_body_schema(endpoint: Endpoint) -> Dict[str, Any]:
    """Assembles the OpenAPI schema for the endpoint body."""
    params = getfullargspec(endpoint.function)
    no_defaults_schema = get_no_defaults_schema(params)
    defaults_schema = get_defaults_schema(params)
    return {
        "type": "object",
        "properties": {**no_defaults_schema, **defaults_schema},
        "additionalProperties": params.varkw is not None,
    }


def get_openapi_endpoint_responses_schema(endpoint: Endpoint) -> Dict[str, Any]:
    """Assembles the OpenAPI schema for the endpoint responses."""
    params = getfullargspec(endpoint.function)
    response_type = "AcceptedOperation" if endpoint.callback else "SuccesfulOperation"
    responses: Dict[str, Any] = {
        f"{endpoint.response_code}": {
            "$ref": f"#/components/responses/{response_type}"
        },
        "500": {"$ref": "#/components/responses/InternalError"},
    }
    if endpoint.callback is False and "return" in params.annotations:
        responses[f"{endpoint.response_code}"]["content"] = {
            "application/json": {
                "schema": {"type": type_to_string(params.annotations["return"])}
            }
        }
    return responses


# def get_openapi_endpoint_schema(route_dict: Dict[str, Endpoint]) -> Dict[str, Any]:
#     """
#     Generate the OpenAPI documentation for dictionary of endpoints for a specific route.
#     """
#     route_schema = {}
#     for http_method, endpoint in route_dict.items():
#         body_schema = get_openapi_endpoint_body_schema(endpoint)
#         responses_schema = get_openapi_endpoint_responses_schema(endpoint)
#         route_schema[http_method.lower()] = {
#             "description": endpoint.docstring,
#             "responses": responses_schema,
#         }
#         has_properties = bool(body_schema["properties"])
#         has_body = has_properties or bool(body_schema["additionalProperties"])
#         if has_body:
#             route_schema[http_method.lower()]["requestBody"] = {
#                 "required": has_properties,
#                 "content": {"application/json": {"schema": body_schema}},
#             }
#     return route_schema


# def get_openapi(sym_obj, title, version="0.0.1", openapi_version="3.0.3"):
#     """
#     Gets the OpenAPI spec of every endpoint and assembles it into a
#     JSON formatted object.
#     """
#     return {
#         "openapi": openapi_version,
#         "info": {
#             "title": title,
#             "version": version
#         },
#         "paths": functools.reduce(
#             lambda x, y: {**x, **y},
#             [get_openapi_endpoint(endpoint) for endpoint in sym_obj.endpoints
#                 if symmetric.openapi.helpers.is_not_docs(endpoint.route)],
#             {}
#         ),
#         "components": {
#             "securitySchemes": {
#                 "APIKeyAuth": {
#                     "type": "apiKey",
#                     "in": "header",
#                     "name": sym_obj.client_token_name
#                 }
#             },
#             "responses": {
#                 "SuccesfulOperation": {
#                     "description": "Successful operation"
#                 },
#                 "UnauthorizedError": {
#                     "description": "Invalid or non-existent authentication "
#                                    "credentials."
#                 },
#                 "InternalError": {
#                     "description": "Unexpected internal error (API method "
#                                    "failed, probably due to a missuse of the "
#                                    "underlying function)."
#                 }
#             }
#         }
#     }