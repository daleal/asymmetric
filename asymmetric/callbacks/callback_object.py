"""
A module for asymmetric's callback schemas.
"""


CALLBACK_OBJECT_SCHEMA = {
    "callback_url_header": {
        "required": False,
        "type": str,
    },
    "callback_method_header": {
        "required": False,
        "type": str,
    },
    "custom_callback_key_header": {
        "required": False,
        "type": str,
    },
}


CALLBACK_OBJECT_DEFAULTS = {
    "callback_url_header": "asymmetric_callback_url",
    "callback_method_header": "asymmetric_callback_method",
    "custom_callback_key_header": "asymmetric_custom_callback_key",
}


CALLBACK_OBJECT_METADATA = {
    "callback_url_header": {
        "required": True,
        "description": "URL to the API to send the function response data.",
    },
    "callback_method_header": {
        "required": False,
        "description": (
            "HTTP method to use when making the callback request. Defaults to POST."
        ),
    },
    "custom_callback_key_header": {
        "required": False,
        "description": (
            "Key to wrap the function output around. By default, "
            "the output won't be wrapped."
        ),
    },
}
