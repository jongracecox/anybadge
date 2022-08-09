import logging
import urllib.parse as urlparse
from http.server import BaseHTTPRequestHandler

from anybadge import Badge

logger = logging.getLogger(__name__)


class AnyBadgeHTTPRequestHandler(BaseHTTPRequestHandler):
    """Request handler for anybadge HTTP server."""

    def do_HEAD(self):
        logging.debug("Sending head.")
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        logging.debug("Handling get request.")
        self.do_HEAD()

        # Ignore request for favicon
        if self.path == "/favicon.ico":
            logging.debug("Ignoring favicon request.")
            return

        # Parse the URL query string
        parsed = urlparse.urlparse(self.path)
        url_query = urlparse.parse_qs(parsed.query)

        label = ""
        value = ""
        color = "green"

        # Extract the label and value portions
        if "label" in url_query:
            label = url_query["label"][0]

        if "value" in url_query:
            value = url_query["value"][0]

        logging.debug("Label: %s Value: %s", label, value)

        if label and value and color:
            logging.debug("All parameters present.")
            badge = Badge(label=label, value=value, default_color=color)
            for line in badge.badge_svg_text:
                self.wfile.write(str.encode(line))

        else:
            logging.debug("Not all parameters present.")

            self.wfile.write(b"<html><head><title>Anybadge Web Server.</title></head>")
            self.wfile.write(b"<body>")

            listen_host, listen_port = self.server.server_address

            help_text = f"""
                        <h1>Welcome to the Anybadge Web Server.</h1>

                        You are seeing this message because you haven't passed all the query parameters
                        to display a badge.

                        You need to pass at least a <b>label</b> and <b>value</b> parameter.

                        Here is an example:

                        <a href="http://{listen_host}:{listen_port}/?label=Project%20Awesomeness&value=110%">\
                        http://{listen_host}:{listen_port}/?label=Project%20Awesomeness&value=110%</a>
                        """

            for line in help_text.splitlines():
                self.wfile.write(str.encode("<p>%s</p>" % line))
            self.wfile.write(b"</body></html>")
