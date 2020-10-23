"""
A module for asymmetric's callback utilities.
"""

from typing import Any, Dict, Union

from asymmetric.callbacks.callback_object import CALLBACK_OBJECT_SCHEMA
from asymmetric.utils import valid_plain_dict


def valid_callback_data(callback: Union[Dict[str, Any], bool]) -> bool:
    """
    Returns a boolean indicating if the callback object is a valid json
    conforming to the json schema.
    """
    if isinstance(callback, bool):
        return True
    return valid_plain_dict(callback, CALLBACK_OBJECT_SCHEMA)
