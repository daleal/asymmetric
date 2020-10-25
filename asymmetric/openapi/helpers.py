"""
A module for every helper of the OpenAPI documentation generator.
"""

from typing import Any


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
