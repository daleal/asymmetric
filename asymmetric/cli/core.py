"""
A module to route the CLI traffic.
"""

from argparse import ArgumentParser

import asymmetric


def dispatcher() -> None:
    """
    Main CLI method, recieves the command line action and dispatches it to
    the corresponding method.
    """
    parser = generate_parser()
    parser.parse_args()


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

    return parser
