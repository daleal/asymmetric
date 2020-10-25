"""
A module for asymmetric's callback utilities.
"""

import json
from typing import Any, Dict, Union

from asymmetric.callbacks.callback_object import (
    CALLBACK_OBJECT_DEFAULTS,
    CALLBACK_OBJECT_SCHEMA,
)
from asymmetric.errors import InvalidCallbackObjectError
from asymmetric.utils import valid_plain_dict


def valid_callback_data(callback: Union[Dict[str, Any], bool]) -> bool:
    """
    Returns a boolean indicating if the callback object is a valid json
    conforming to the json schema.
    """
    if isinstance(callback, bool):
        return True
    return valid_plain_dict(callback, CALLBACK_OBJECT_SCHEMA)


def validate_callback_data(callback: Union[Dict[str, Any], bool]) -> None:
    """Raises an error if the callback data is not valid."""
    if not valid_callback_data(callback):
        raise InvalidCallbackObjectError(
            "Invalid callback object:\n"
            + json.dumps(callback, indent=2, sort_keys=False, ensure_ascii=False)
        )


def get_header_finders(callback: Union[Dict[str, Any], bool]) -> Dict[str, str]:
    """Gets the header finders. Returns the default ones if it doesn't find some."""
    if isinstance(callback, bool):
        # Callback attribute is True
        return CALLBACK_OBJECT_DEFAULTS
    # Callback attribute is an object, get callback attribute finders
    return {
        k: callback[k] if k in callback else default_value
        for k, default_value in CALLBACK_OBJECT_DEFAULTS.items()
    }
