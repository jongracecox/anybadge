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
        logo = ""
        logo_color = ""
        logo_position = ""
        logos_dirs = getattr(self.server, "logos_dirs", []) or []

        # Extract the label and value portions
        if "label" in url_query:
            label = url_query["label"][0]

        if "value" in url_query:
            value = url_query["value"][0]

        if "logo" in url_query:
            logo = url_query["logo"][0]

        if "logo_color" in url_query:
            logo_color = url_query["logo_color"][0]

        if "logo_position" in url_query:
            logo_position = url_query["logo_position"][0]

        logging.debug("Label: %s Value: %s", label, value)

        if label and value and color:
            logging.debug("All parameters present.")
            try:
                badge = Badge(
                    label=label,
                    value=value,
                    default_color=color,
                    logo=logo,
                    logo_color=logo_color,
                    logo_position=logo_position if logo else None,
                    logo_dirs=logos_dirs,
                )
            except ValueError as e:
                logger.debug("Badge generation failed: %s", e)
                self.send_response(400)
                self.send_header("Content-type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write(str.encode("ERROR: %s\n" % e))
                return
            self.wfile.write(str.encode(badge.badge_svg_text))

        else:
            logging.debug("Not all parameters present.")

            self.wfile.write(b"<html><head><title>Anybadge Web Server.</title></head>")
            self.wfile.write(b"<body>")

            listen_host, listen_port = self.server.server_address

            help_text = f"""
                        <h1>Welcome to the Anybadge Web Server.</h1>

                        You are seeing this message because you haven't passed all the query parameters
                        to display a badge.

                        You need to pass at least a <b>label</b> and <b>value</b> parameter. You may also
                        pass optional <b>logo</b> (logo name, path or URL), <b>logo_color</b> and
                        <b>logo_position</b> (left/right) parameters. Logos are resolved from the
                        server's configured logos directories, the logos bundled with anybadge, then
                        the network.

                        Here is an example:

                        <a href="http://{listen_host}:{listen_port}/?label=Project%20Awesomeness&value=110%\
&logo=python">\
                        http://{listen_host}:{listen_port}/?label=Project%20Awesomeness&value=110%&logo=python\
                        </a>
                        """

            for line in help_text.splitlines():
                self.wfile.write(str.encode("<p>%s</p>" % line))
            self.wfile.write(b"</body></html>")
