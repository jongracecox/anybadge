import argparse
import logging
from http.server import HTTPServer
from os import environ
from typing import Optional, Tuple

from anybadge.server.request_handler import AnyBadgeHTTPRequestHandler
from anybadge.server import config

logger = logging.getLogger(__name__)


def run(listen_address: Optional[str] = None, port: Optional[int] = None):
    """Run a persistent webserver."""
    if not listen_address:
        listen_address = config.DEFAULT_SERVER_LISTEN_ADDRESS

    if not port:
        port = config.DEFAULT_SERVER_PORT

    server_address: Tuple[str, int] = (listen_address, port)  # type: ignore

    httpd = HTTPServer(server_address, AnyBadgeHTTPRequestHandler)
    logger.info("Serving at: http://%s:%s" % server_address)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt. Shutting down...")


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    logger.debug("Parsing command line arguments.")
    parser = argparse.ArgumentParser(description="Run an anybadge server.")
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=config.DEFAULT_SERVER_PORT,
        help=f"Server port number.  Default is {config.DEFAULT_SERVER_PORT}. This can also be set via an environment "
        "variable called ``ANYBADGE_PORT``.",
    )
    parser.add_argument(
        "-l",
        "--listen-address",
        type=str,
        default=config.DEFAULT_SERVER_LISTEN_ADDRESS,
        help=f"Server listen address.  Default is {config.DEFAULT_SERVER_LISTEN_ADDRESS}. This can also be set via an "
        f"environment variable called ``ANYBADGE_LISTEN_ADDRESS``.",
    )
    parser.add_argument(
        "-d", "--debug", action="store_true", help="Enable debug logging."
    )
    return parser.parse_args()


def main() -> None:
    """Run server."""

    # Check for environment variables
    if "ANYBADGE_PORT" in environ:
        port = environ["ANYBADGE_PORT"]
        try:
            port_int = int(port)
        except ValueError:
            logger.error(
                "ANYBADGE_PORT environment variable must be an integer. Got %s", port
            )
            raise
        config.DEFAULT_SERVER_PORT = port_int

    if "ANYBADGE_LISTEN_ADDRESS" in environ:
        config.DEFAULT_SERVER_LISTEN_ADDRESS = environ["ANYBADGE_LISTEN_ADDRESS"]

    if "ANYBADGE_LOG_LEVEL" in environ:
        config.DEFAULT_LOGGING_LEVEL = logging.getLevelName(
            environ["ANYBADGE_LOG_LEVEL"]
        )

    # Parse command line args
    args: argparse.Namespace = parse_args()

    # Set logging level
    logging_level = config.DEFAULT_LOGGING_LEVEL
    if args.debug:
        logging_level = logging.DEBUG

    logging.basicConfig(
        format="%(asctime)-15s %(levelname)s:%(filename)s(%(lineno)d):%(funcName)s: %(message)s",
        level=logging_level,
    )
    logger.info("Starting up anybadge server.")

    run(listen_address=args.listen_address, port=args.port)


if __name__ == "__main__":
    main()
