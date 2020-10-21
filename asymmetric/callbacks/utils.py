"""
A module for asymmetric's callback utilities.
"""

import jsonschema

from asymmetric.callbacks.callback_object import CALLBACK_OBJECT_SCHEMA


def valid_callback_data(callback):
    """
    Returns a boolean indicating if the callback object is a valid json
    conforming to the json schema.
    """
    if isinstance(callback, bool):
        return True

    try:
        jsonschema.validate(instance=callback, schema=CALLBACK_OBJECT_SCHEMA)
        return True
    except jsonschema.exceptions.ValidationError:
        return False
