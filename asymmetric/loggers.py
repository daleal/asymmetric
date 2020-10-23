"""
A module for containing the loggers of asymmetric.
"""

import json
import logging
import logging.config
import os
from typing import Any, Callable, Dict

from starlette.requests import Request

from asymmetric.constants import LOG_FILE_NAME
from asymmetric.utils import get_body

# Logging configuration
logging.config.dictConfig(
    {
        "version": 1,
        "formatters": {
            "console": {
                "format": "[%(asctime)s] [%(levelname)s] %(module)s: %(message)s"
            },
            "file": {
                "format": (
                    "[%(asctime)s] [%(levelname)s] %(pathname)s - "
                    "line %(lineno)d: \n%(message)s\n"
                )
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
                "formatter": "console",
            },
            "file": {
                "class": "logging.FileHandler",
                "filename": os.getenv("LOG_FILE", default=LOG_FILE_NAME),
                "formatter": "file",
            },
        },
        "root": {"level": "INFO", "handlers": ["console", "file"]},
    }
)


def log(message: str, level: str = "info") -> None:
    """
    Logs {message} with {level} level. Starts the log with '[[asymmetric]]'.
    """
    logger = getattr(logging, level)
    logger(f"[[asymmetric]] {message}")


async def log_request(
    request: Request, route: str, function: Callable[..., Any]
) -> None:
    """
    Logs a request, including the method used for the request, the
    route and the name of the python function being called. Then,
    logs the request body.
    """
    log(
        f"{request.method} request to '{route}' endpoint "
        f"('{function.__name__}' function)."
    )
    log_request_body(await get_body(request))


def log_request_body(body: Dict[str, Any]) -> None:
    """
    Logs a request body formatted as a json.
    """
    log(
        "Request Body:\n"
        + json.dumps(body, indent=2, sort_keys=False, ensure_ascii=False)
    )
