"""
A module to route the CLI traffic.
"""

import sys
from argparse import ArgumentParser, _SubParsersAction
from typing import Any

import asymmetric
from asymmetric.cli.helpers import setup_documentation_arguments, setup_runner_arguments
from asymmetric.cli.utils import document_openapi, start_server


def dispatcher(*args: Any, **kwargs: Any) -> None:
    """
    Main CLI method, recieves the command line action and dispatches it to
    the corresponding method.
    """
    parser = generate_parser()
    parsed_args = parser.parse_args(*args, **kwargs)

    try:
        if parsed_args.action == "run":  # pragma: no cover
            run_args = vars(parsed_args)
            run_args.pop("action")
            module_name = run_args.pop("module")
            start_server(module_name, run_args)
        elif parsed_args.action == "docs":
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

    # Runner parser
    generate_runner_subparser(subparsers)

    # Documentation parser
    generate_documentation_subparser(subparsers)

    return parser


def generate_runner_subparser(subparsers: _SubParsersAction) -> ArgumentParser:
    """Generates the subparser for the run server option."""
    runner_parser = subparsers.add_parser("run")
    runner_parser.set_defaults(action="run")
    return setup_runner_arguments(runner_parser)


def generate_documentation_subparser(subparsers: _SubParsersAction) -> ArgumentParser:
    """Generates the subparser for the auto-documentation option."""
    documentation_parser = subparsers.add_parser("docs")
    documentation_parser.set_defaults(action="docs")
    return setup_documentation_arguments(documentation_parser)
