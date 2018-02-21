#!/usr/bin/python
"""
Anybadge Server

This package provides a server for anybadge.
"""
from __future__ import print_function
from os import environ
import logging
import argparse
from anybadge import Badge

# Import the correct version of HTTP server
try:
    from http.server import HTTPServer, BaseHTTPRequestHandler
except ImportError:
    from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

# Import the correct version of urlparse, depending on which version
# of Python we are using
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse


logger = logging.getLogger(__name__)

DEFAULT_SERVER_PORT = 8000
DEFAULT_SERVER_LISTEN_ADDRESS = 'localhost'
DEFAULT_LOGGING_LEVEL = logging.INFO

SERVER_PORT = DEFAULT_SERVER_PORT
SERVER_LISTEN_ADDRESS = DEFAULT_SERVER_LISTEN_ADDRESS


class AnybadgeHTTPRequestHandler(BaseHTTPRequestHandler):
    """Request handler for Anybadge HTTP server."""

    def do_HEAD(self):
        logging.debug('Sending head.')
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        logging.debug('Handling get request.')
        self.do_HEAD()

        # Ignore request for favicon
        if self.path == '/favicon.ico':
            logging.debug('Ignoring favicon request.')
            return

        # Parse the URL query string
        parsed = urlparse.urlparse(self.path)
        url_query = urlparse.parse_qs(parsed.query)

        label = ''
        value = ''
        color = 'green'

        # Extract the label and value portions
        if 'label' in url_query:
            label = url_query['label'][0]

        if 'value' in url_query:
            value = url_query['value'][0]

        logging.debug('Label: %s Value: %s', label, value)

        if label and value and color:
            logging.debug('All parameters present.')
            badge = Badge(label=label, value=value, default_color=color)
            for line in badge.badge_svg_text:
                self.wfile.write(str.encode(line))
            
        else:
            logging.debug('Not all parameters present.')

            self.wfile.write(b"<html><head><title>Anybadge Web Server.</title></head>")
            self.wfile.write(b"<body>")

            help_text = """
                        <h1>Welcome to the Anybadge Web Server.</h1>

                        You are seeing this message because you haven't passed all the query parameters
                        to display a badge.

                        You need to pass at least a <b>label</b> and <b>value</b> parameter.

                        Here is an example:

                        <a href="http://localhost:{port}/?label=Project%20Awesomeness&value=110%">\
                        http://localhost:{port}/?label=Project%20Awesomeness&value=110%</a>
                        """.format(port=SERVER_PORT)

            for line in help_text.splitlines():
                self.wfile.write(str.encode('<p>%s</p>' % line))
            self.wfile.write(b"</body></html>")


def run(listen_address=DEFAULT_SERVER_LISTEN_ADDRESS, port=DEFAULT_SERVER_PORT):
    server_address = (listen_address, port)

    global SERVER_PORT, SERVER_LISTEN_ADDRESS

    SERVER_PORT = port
    SERVER_LISTEN_ADDRESS = listen_address

    httpd = HTTPServer(server_address, AnybadgeHTTPRequestHandler)
    logging.info('Serving at: http://%s:%s' % server_address)
    httpd.serve_forever()


def parse_args():
    logger.debug('Parsing command line arguments.')
    parser = argparse.ArgumentParser(description="Run an anybadge server.")
    parser.add_argument('-p', '--port', type=int, default=DEFAULT_SERVER_PORT,
                        help="Server port number.  Default is %s.  This can also be set via an environment "
                             "variable called ``ANYBADGE_PORT``." % DEFAULT_SERVER_PORT)
    parser.add_argument('-l', '--listen-address', type=str, default=DEFAULT_SERVER_LISTEN_ADDRESS,
                        help="Server listen address.  Default is %s.  This can also be set via an environment "
                             "variable called ``ANYBADGE_LISTEN_ADDRESS``." % DEFAULT_SERVER_LISTEN_ADDRESS)
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug logging.')
    return parser.parse_args()


def main():
    """Run server."""

    global DEFAULT_SERVER_PORT, DEFAULT_SERVER_LISTEN_ADDRESS, DEFAULT_LOGGING_LEVEL

    # Check for environment variables
    if 'ANYBADGE_PORT' in environ:
        DEFAULT_SERVER_PORT = environ['ANYBADGE_PORT']

    if 'ANYBADGE_LISTEN_ADDRESS' in environ:
        DEFAULT_SERVER_LISTEN_ADDRESS = environ['ANYBADGE_LISTEN_ADDRESS']

    if 'ANYBADGE_LOG_LEVEL' in environ:
        DEFAULT_LOGGING_LEVEL = logging.getLevelName(environ['ANYBADGE_LOG_LEVEL'])

    # Parse command line args
    args = parse_args()

    # Set logging level
    logging_level = DEFAULT_LOGGING_LEVEL
    if args.debug:
        logging_level = logging.DEBUG

    logging.basicConfig(format='%(asctime)-15s %(levelname)s:%(filename)s(%(lineno)d):%(funcName)s: %(message)s',
                        level=logging_level)
    logger.info('Starting up anybadge server.')

    run(listen_address=args.listen_address, port=args.port)


if __name__ == '__main__':
    main()