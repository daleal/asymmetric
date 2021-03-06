"""
A module to hold some CLI utilities.
"""

import json
import os
import sys
from importlib import import_module
from traceback import print_exception
from types import ModuleType
from typing import Any, Dict

import uvicorn  # type: ignore

from asymmetric.cli.helpers import clear_runner_args
from asymmetric.core import _Asymmetric
from asymmetric.errors import AppImportError
from asymmetric.helpers import humanize
from asymmetric.loggers import configure_loggers
from asymmetric.openapi.core import get_openapi


def start_server(module: str, arguments: Dict[str, Any]) -> None:  # pragma: no cover
    """
    Tries to find the asymmetric object and then runs an uvicorn server
    with the parameters given to the method.
    """
    # Check that the application exists
    get_asymmetric_object(module)

    # Get filtered arguments
    run_args = clear_runner_args(arguments)

    if "log_level" in run_args:
        # Set the logging level to the one of the command
        os.environ["LOG_LEVEL"] = run_args["log_level"].upper()
        configure_loggers()

    uvicorn.run(f"{module}:asymmetric", **run_args)


def document_openapi(module: str, filename: str) -> None:
    """
    Gets the asymmetric object and then calls the OpenAPI spec generator method.
    """
    asymmetric_object = get_asymmetric_object(module)
    docs = get_openapi(asymmetric_object, f"{humanize(module)} API")
    with open(filename, "w") as docs_file:
        json.dump(docs, docs_file, indent=2)


def get_main_module(module_name: str) -> ModuleType:
    """
    Imports the module :module_name and returns it. This method is strongly
    inspired in gunicorn's own import_app method and uvicorn's main method.
    """
    try:
        # Add current directory to path
        sys.path.insert(0, ".")
        return import_module(module_name)
    except ImportError as error:
        # If the user wrote module.py instead of just module
        if module_name.endswith(".py") and os.path.exists(module_name):
            actual_name = module_name.rsplit(".", 1)[0]
            error_str = f"Module {module_name} not found. Did you mean {actual_name}?"
            raise ImportError(error_str) from error
        raise


def get_asymmetric_object(module_name: str, debug: bool = True) -> _Asymmetric:
    """
    Imports the module :module_name and the tries to find the
    asymmetric object. This method is strongly inspired in gunicorn's own
    import_app method and uvicorn's main method.
    """
    # Import the module
    module = get_main_module(module_name)

    # Get the asymmetric object
    try:
        return getattr(module, "asymmetric")
    except AttributeError as error:
        if debug:
            print_exception(*sys.exc_info())
        error_str = f"Failed to find the asymmetric object in {module_name}."
        raise AppImportError(error_str) from error
