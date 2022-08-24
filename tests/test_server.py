import subprocess
import time

import requests  # type: ignore
from unittest import TestCase


class TestAnybadgeServer(TestCase):
    """Test case class for anybadge server."""

    def setUp(self):
        if not hasattr(self, "assertRaisesRegex"):
            self.assertRaisesRegex = self.assertRaisesRegexp
        self.proc = subprocess.Popen(
            ["anybadge-server", "-p", "8000", "--listen-address", "127.0.0.1"],
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        time.sleep(1)

    def tearDown(self) -> None:
        self.proc.kill()

    def test_server_is_running(self):
        """Test that the server is running."""
        self.assertTrue(self.proc.pid > 0)

    def test_server_root_request(self):
        """Test that the server can be accessed."""
        url = "http://127.0.0.1:8000"
        response = requests.get(url)
        self.assertTrue(response.ok)
        self.assertTrue(
            response.content.startswith(b"<html><head><title>Anybadge Web Server.")
        )

    def test_server_badge_request(self):
        """Test that the server can be accessed."""
        url = "http://127.0.0.1:8000/?label=Project%20Awesomeness&value=110%"
        response = requests.get(url)
        self.assertTrue(response.ok)
        print(response.content)
        self.assertTrue(
            response.content.startswith(b'<?xml version="1.0" encoding="UTF-8"?>\n<svg')
        )

    def test_server_module_same_output_as_server_cli(self):
        """Test that `python -m anybadge.server` is equivalent to calling `anybadge-server` directly."""
        output_module = subprocess.check_output(
            ["python", "-m", "anybadge.server", "--help"]
        )
        output_script = subprocess.check_output(["anybadge-server", "--help"])
        self.assertEqual(output_module, output_script)
