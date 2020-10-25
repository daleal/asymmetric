"""
A module for every helper of the OpenAPI documentation generator.
"""

from typing import Any

from asymmetric.constants import (
    OPENAPI_SPEC_ROUTE,
    REDOC_DOCUMENTATION_ROUTE,
    SWAGGER_DOCUMENTATION_ROUTE,
)


def type_to_string(type_obj: Any) -> str:
    """Given a python type, return its JSON schema string counterpart."""
    try:
        type_str = type_obj.__name__
        if type_str == "str":
            return "string"
        if type_str == "float":
            return "number"
        if type_str == "int":
            return "integer"
        if type_str == "bool":
            return "boolean"
        if type_str == "NoneType":
            return "null"
        if type_str == "list":
            return "array"
        return "object"
    except Exception:
        return "object"


def is_not_docs(route: str) -> bool:
    """Checks if a route is not a documentation-related route."""
    # Check that the route is not the schema route
    not_schema = route != OPENAPI_SPEC_ROUTE
    # Check that the route is not the Swagger interactive documentation route
    not_swagger_documentation = route != SWAGGER_DOCUMENTATION_ROUTE
    # Check that the route is not the ReDoc interactive documentation route
    not_redoc_documentation = route != REDOC_DOCUMENTATION_ROUTE

    # Return if the route is neither of the documentation routes
    return not_schema and not_swagger_documentation and not_redoc_documentation
