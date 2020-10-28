"""
A module for every helper of the asymmetric CLI.
"""

from argparse import ArgumentParser
from typing import Any, Dict


def clear_runner_args(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Given an args object, return a dictionary with the keys and values of only the
    non-None values of the original object.
    """
    return {k: v for k, v in args.items() if v is not None}


def setup_documentation_arguments(
    documentation_parser: ArgumentParser,
) -> ArgumentParser:
    """Setup the arguments for the documentation parser for the asymmetric CLI."""
    # Module name
    documentation_parser.add_argument(
        "module",
        metavar="module",
        help="Name of the module that uses the asymmetric object.",
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


def setup_runner_arguments(runner_parser: ArgumentParser) -> ArgumentParser:
    """Setup the arguments for the runner parser for the asymmetric CLI."""
    # Module name
    runner_parser.add_argument(
        "module",
        metavar="module",
        help="Name of the module that uses the asymmetric object.",
    )

    # Host
    runner_parser.add_argument(
        "--host",
        dest="host",
        default=None,
        help="Bind socket to this host. [default: 127.0.0.1]",
    )

    # Port
    runner_parser.add_argument(
        "--port",
        dest="port",
        type=int,
        default=None,
        help="Bind socket to this port. [default: 8000]",
    )

    # Unix Domain Socket
    runner_parser.add_argument(
        "--uds",
        dest="uds",
        default=None,
        help="Bind to a UNIX domain socket.",
    )

    # File Descriptor
    runner_parser.add_argument(
        "--fd",
        dest="fd",
        type=int,
        default=None,
        help="Bind to socket from this file descriptor.",
    )

    # Reload
    runner_parser.add_argument(
        "--reload",
        dest="reload",
        action="store_const",
        default=False,
        const=True,
        help="Enable auto-reload.",
    )

    # Reload Directory
    runner_parser.add_argument(
        "--reload-dir",
        dest="reload_dir",
        default=None,
        help=(
            "Set reload directories explicitly, instead of using the "
            "current working directory."
        ),
    )

    # Workers
    runner_parser.add_argument(
        "--workers",
        dest="workers",
        type=int,
        default=None,
        help=(
            "Number of worker processes. Defaults to the $WEB_CONCURRENCY "
            "environment variable if available. Not valid with --reload."
        ),
    )

    # Loop
    runner_parser.add_argument(
        "--loop",
        dest="loop",
        default=None,
        help="Event loop implementation. [default: auto]",
    )

    # HTTP
    runner_parser.add_argument(
        "--http",
        dest="http",
        default=None,
        help="HTTP protocol implementation. [default: auto]",
    )

    # WebSocket
    runner_parser.add_argument(
        "--ws",
        dest="ws",
        default=None,
        help="WebSocket protocol implementation. [default: auto]",
    )

    # Lifespan
    runner_parser.add_argument(
        "--lifespan",
        dest="lifespan",
        default=None,
        help="Lifespan implementation. [default: auto]",
    )

    # Interface
    runner_parser.add_argument(
        "--interface",
        dest="interface",
        default=None,
        help=(
            "Select ASGI3, ASGI2, or WSGI as the application "
            "interface. [default: auto]"
        ),
    )

    # env file
    runner_parser.add_argument(
        "--env-file",
        dest="env_file",
        default=None,
        help="Environment configuration file.",
    )

    # Log config
    runner_parser.add_argument(
        "--log-config",
        dest="log_config",
        default=None,
        help="Logging configuration file. Supported formats (.ini, .json, .yaml)",
    )

    # Log level
    runner_parser.add_argument(
        "--log-level",
        dest="log_level",
        default=None,
        help="Log level. [default: info]",
    )

    # Enable access logs
    runner_parser.add_argument(
        "--access-log",
        dest="access_log",
        help="Enable access log.",
    )

    # Disable access logs
    runner_parser.add_argument(
        "--no-access-log",
        dest="no_access_log",
        help="Disable access log.",
    )

    # Enable colorized logging
    runner_parser.add_argument(
        "--use-colors",
        dest="use_colors",
        help="Enable colorized logging.",
    )

    # Disable colorized logging
    runner_parser.add_argument(
        "--no-use-colors",
        dest="no_use_colors",
        help="Disable colorized logging.",
    )

    # Enable proxy headers
    runner_parser.add_argument(
        "--proxy-headers",
        dest="proxy_headers",
        help=(
            "Enable X-Forwarded-Proto, X-Forwarded-For, X-Forwarded-Port to "
            "populate remote address info."
        ),
    )

    # Disable proxy headers
    runner_parser.add_argument(
        "--no-proxy-headers",
        dest="no_proxy_headers",
        help=(
            "Disable X-Forwarded-Proto, X-Forwarded-For, X-Forwarded-Port to "
            "populate remote address info."
        ),
    )

    # Forwarded allow IPs
    runner_parser.add_argument(
        "--forwarded-allow-ips",
        dest="forwarded_allow_ips",
        default=None,
        help=(
            "Comma seperated list of IPs to trust with proxy headers. Defaults "
            "to the $FORWARDED_ALLOW_IPS environment variable if available, "
            "or '127.0.0.1'."
        ),
    )

    # Root path
    runner_parser.add_argument(
        "--root-path",
        dest="root_path",
        default=None,
        help=(
            "Set the ASGI 'root_path' for applications submounted below "
            "a given URL path."
        ),
    )

    # Limit concurrency
    runner_parser.add_argument(
        "--limit-concurrency",
        dest="limit_concurrency",
        type=int,
        default=None,
        help=(
            "Maximum number of concurrent connections or tasks to allow, "
            "before issuing HTTP 503 responses."
        ),
    )

    # Backlog
    runner_parser.add_argument(
        "--backlog",
        dest="backlog",
        type=int,
        default=None,
        help="Maximum number of connections to hold in backlog",
    )

    # Limit max requests
    runner_parser.add_argument(
        "--limit-max-requests",
        dest="limit_max_requests",
        type=int,
        default=None,
        help="Maximum number of requests to service before terminating the process.",
    )

    # Timeout keep alive
    runner_parser.add_argument(
        "--timeout-keep-alive",
        dest="timeout_keep_alive",
        type=int,
        default=None,
        help=(
            "Close Keep-Alive connections if no new data is received within "
            "this timeout. [default: 5]"
        ),
    )

    # SSL KeyFile
    runner_parser.add_argument(
        "--ssl-keyfile",
        dest="ssl_keyfile",
        default=None,
        help="SSL key file",
    )

    # SSL Certificate
    runner_parser.add_argument(
        "--ssl-certfile",
        dest="ssl_certfile",
        default=None,
        help="SSL certificate file",
    )

    # SSL KeyFile Password
    runner_parser.add_argument(
        "--ssl-keyfile-password",
        dest="ssl_keyfile_password",
        default=None,
        help="SSL key file password",
    )

    # SSL version
    runner_parser.add_argument(
        "--ssl-version",
        dest="ssl_version",
        type=int,
        default=None,
        help="SSL version to use (see stdlib ssl module's) [default: 2]",
    )

    # SSL Certificate requests
    runner_parser.add_argument(
        "--ssl-cert-reqs",
        dest="ssl_cert_reqs",
        type=int,
        default=None,
        help=(
            "Whether client certificate is required (see stdlib ssl "
            "module's) [default: 0]"
        ),
    )

    # CA certificates
    runner_parser.add_argument(
        "--ssl-ca-certs",
        dest="ssl_ca_certs",
        default=None,
        help="CA certificates file",
    )

    # Ciphers
    runner_parser.add_argument(
        "--ssl-ciphers",
        dest="ssl_ciphers",
        default=None,
        help="Ciphers to use (see stdlib ssl module's) [default: TLSv1]",
    )

    # HTTP response headers
    runner_parser.add_argument(
        "--header",
        dest="header",
        default=None,
        help="Specify custom default HTTP response headers as a Name:Value pair",
    )

    # App directory
    runner_parser.add_argument(
        "--app-dir",
        dest="app_dir",
        default=None,
        help=(
            "Look for APP in the specified directory, "
            "by adding this to the PYTHONPATH. Defaults "
            "to the current working directory."
        ),
    )

    return runner_parser
