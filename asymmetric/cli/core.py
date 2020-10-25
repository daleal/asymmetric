"""
A module to route the CLI traffic.
"""

import sys
from argparse import ArgumentParser, _SubParsersAction
from typing import Any

import asymmetric
from asymmetric.cli.utils import document_openapi


def dispatcher(*args: Any, **kwargs: Any) -> None:
    """
    Main CLI method, recieves the command line action and dispatches it to
    the corresponding method.
    """
    parser = generate_parser()
    parsed_args = parser.parse_args(*args, **kwargs)

    try:
        if parsed_args.action == "docs":
            document_openapi(parsed_args.module, parsed_args.filename)
    except AttributeError:
        print("An argument is required for the asymmetric command.")
        parser.print_help()
        sys.exit(1)


def generate_parser() -> ArgumentParser:
    """Generates the CLI parser for the module."""
    # Create parser
    parser = ArgumentParser(description="Command line interface tool for asymmetric.")

    # Add version command
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"asymmetric version {asymmetric.__version__}",
    )

    # In order to allow the CLI utility grow, the parser will include an
    # initial argumment to determine which subparser will be executed.

    # Create subparsers
    subparsers = parser.add_subparsers(help="Action to be executed.")

    # Documentation parser
    generate_documentation_subparser(subparsers)

    return parser


def generate_documentation_subparser(subparsers: _SubParsersAction) -> ArgumentParser:
    """Generates the subparser for the auto-documentation option."""
    documentation_parser = subparsers.add_parser("docs")
    documentation_parser.set_defaults(action="docs")

    # Module name
    documentation_parser.add_argument(
        "module",
        metavar="module",
        help="Name of the module that uses the symmetric object.",
    )

    # Filename
    documentation_parser.add_argument(
        "-f",
        "--filename",
        dest="filename",
        default="openapi.json",
        help="Name of the file in where to write the OpenAPI documentation spec.",
    )

    return documentation_parser
