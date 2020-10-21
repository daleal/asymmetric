"""
A module for asymmetric's callback schemas.
"""


CALLBACK_OBJECT_SCHEMA = {
    "type": "object",
    "properties": {
        "callback_url_header": {
            "type": "string",
        },
        "callback_method_header": {
            "type": "string",
        },
        "custom_callback_key_header": {
            "type": "string",
        },
    },
}


CALLBACK_OBJECT_DEFAULTS = {
    "callback_url_header": "asymmetric_callback_url",
    "callback_method_header": "asymmetric_callback_method",
    "custom_callback_key_header": "asymmetric_custom_callback_key",
}
