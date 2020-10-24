"""
A module for containing the singleton metaclass for the _Asymmetric class.
"""

from typing import Any


class AsymmetricSingleton(type):

    """
    Singleton metaclass to limit the existance of the asymmetric object to one.
    """

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        """Defines the class creation method."""
        if not hasattr(cls, "asymmetric_instance"):  # Object does not exist
            cls.asymmetric_instance = super().__call__(*args, **kwargs)  # Create object
        return cls.asymmetric_instance  # Return asymmetric object
