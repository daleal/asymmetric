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
