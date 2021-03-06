"""
Module to hold every custom exception.
"""


class DuplicatedEndpointError(Exception):
    """
    Exception for when an endpoint is already in the added endpoints.
    """


class InvalidCallbackObjectError(Exception):
    """
    Exception for when the callback object is incorrectly formed.
    """


class InvalidCallbackHeadersError(Exception):
    """
    Exception for when the callback headers are incorrect.
    """


class AppImportError(Exception):
    """
    Exception for when there's an error finding the asymmetric object inside
    the specified module.
    """
