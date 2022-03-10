import argparse
import logging
from http.server import HTTPServer
from os import environ

from anybadge.server.request_handler import AnyBadgeHTTPRequestHandler
from anybadge.server import config

logger = logging.getLogger(__name__)


def run(listen_address: str = None, port: int = None):
    if not listen_address:
        listen_address = config.DEFAULT_SERVER_LISTEN_ADDRESS

    if not port:
        port = config.DEFAULT_SERVER_PORT

    server_address = (listen_address, port)

    global SERVER_PORT, SERVER_LISTEN_ADDRESS

    SERVER_PORT = port
    SERVER_LISTEN_ADDRESS = listen_address

    httpd = HTTPServer(server_address, AnyBadgeHTTPRequestHandler)
    logger.info("Serving at: http://%s:%s" % server_address)
    httpd.serve_forever()


def parse_args():
    logger.debug("Parsing command line arguments.")
    parser = argparse.ArgumentParser(description="Run an anybadge server.")
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=DEFAULT_SERVER_PORT,
        help="Server port number.  Default is %s.  This can also be set via an environment "
        "variable called ``ANYBADGE_PORT``." % DEFAULT_SERVER_PORT,
    )
    parser.add_argument(
        "-l",
        "--listen-address",
        type=str,
        default=DEFAULT_SERVER_LISTEN_ADDRESS,
        help="Server listen address.  Default is %s.  This can also be set via an environment "
        "variable called ``ANYBADGE_LISTEN_ADDRESS``." % DEFAULT_SERVER_LISTEN_ADDRESS,
    )
    parser.add_argument(
        "-d", "--debug", action="store_true", help="Enable debug logging."
    )
    return parser.parse_args()


def main():
    """Run server."""

    global DEFAULT_SERVER_PORT, DEFAULT_SERVER_LISTEN_ADDRESS, DEFAULT_LOGGING_LEVEL

    # Check for environment variables
    if "ANYBADGE_PORT" in environ:
        DEFAULT_SERVER_PORT = environ["ANYBADGE_PORT"]

    if "ANYBADGE_LISTEN_ADDRESS" in environ:
        DEFAULT_SERVER_LISTEN_ADDRESS = environ["ANYBADGE_LISTEN_ADDRESS"]

    if "ANYBADGE_LOG_LEVEL" in environ:
        DEFAULT_LOGGING_LEVEL = logging.getLevelName(environ["ANYBADGE_LOG_LEVEL"])

    # Parse command line args
    args = parse_args()

    # Set logging level
    logging_level = DEFAULT_LOGGING_LEVEL
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
