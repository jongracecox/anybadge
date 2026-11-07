import os
import shutil
import socket
import subprocess
import sys
import time
import unittest
from pathlib import Path

import requests  # type: ignore
from unittest import TestCase

SERVER_EXECUTABLE_NAME = "anybadge-server.exe" if os.name == "nt" else "anybadge-server"


def _find_server_executable():
    """Locate the anybadge-server command.

    Checks next to the running Python interpreter first (so tests work with
    an unactivated virtualenv), then falls back to the PATH.
    """
    alongside = Path(sys.executable).parent / SERVER_EXECUTABLE_NAME
    if alongside.exists():
        return str(alongside)
    return shutil.which("anybadge-server")


SERVER_EXECUTABLE = _find_server_executable()


def _get_free_port():
    """Return an unused TCP port on localhost.

    There is a small race between closing the probe socket and the server
    binding to it, but it is far less fragile than a fixed port.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return sock.getsockname()[1]


@unittest.skipUnless(
    SERVER_EXECUTABLE,
    "The anybadge-server command is not installed (e.g. pip install .)",
)
class TestAnybadgeServer(TestCase):
    """Test case class for anybadge server."""

    def setUp(self):
        if not hasattr(self, "assertRaisesRegex"):
            self.assertRaisesRegex = self.assertRaisesRegexp
        self.port = _get_free_port()
        self.url = "http://127.0.0.1:%s" % self.port
        self.proc = subprocess.Popen(
            [
                SERVER_EXECUTABLE,
                "-p",
                str(self.port),
                "--listen-address",
                "127.0.0.1",
            ],
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        self._wait_for_server()

    def tearDown(self) -> None:
        self.proc.terminate()
        self.proc.wait(timeout=5)

    def _wait_for_server(self, timeout: float = 10.0) -> None:
        """Wait until the started server accepts connections, or fail."""
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if self.proc.poll() is not None:
                self.fail("anybadge-server exited before accepting connections.")
            try:
                requests.get(self.url, timeout=1)
                return
            except requests.exceptions.ConnectionError:
                time.sleep(0.1)
        self.fail("Server did not start listening within %s seconds" % timeout)

    def test_server_is_running(self):
        """Test that the server is running."""
        self.assertTrue(self.proc.pid > 0)

    def test_server_root_request(self):
        """Test that the server can be accessed."""
        response = requests.get(self.url)
        self.assertTrue(response.ok)
        self.assertTrue(
            response.content.startswith(b"<html><head><title>Anybadge Web Server.")
        )

    def test_server_badge_request(self):
        """Test that the server can be accessed."""
        url = self.url + "/?label=Project%20Awesomeness&value=110%"
        response = requests.get(url)
        self.assertTrue(response.ok)
        # Normalize line endings so the assertion does not depend on the
        # line-ending style of the SVG templates on disk (CRLF on Windows
        # checkouts with autocrlf).
        content = response.content.replace(b"\r\n", b"\n")
        self.assertTrue(
            content.startswith(b'<?xml version="1.0" encoding="UTF-8"?>\n<svg')
        )

    def test_server_module_same_output_as_server_cli(self):
        """Test that `python -m anybadge.server` is equivalent to calling `anybadge-server` directly."""
        output_module = subprocess.check_output(
            [sys.executable, "-m", "anybadge.server", "--help"]
        )
        output_script = subprocess.check_output([SERVER_EXECUTABLE, "--help"])
        self.assertEqual(output_module, output_script)
