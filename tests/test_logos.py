import base64
import os
import sys
import tempfile
from pathlib import Path
from unittest import TestCase, mock

from anybadge import Badge, config, logos
from anybadge.cli import main

TESTS_DIR = Path(__file__).parent
PROJECT_ROOT = TESTS_DIR.parent


class TestBadgeLogos(TestCase):
    """Test case class for badge logo support."""

    # Base64-encoded 1x1 red PNG image, used as a test raster image.
    PNG_BASE64 = (
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk"
        "yPhWDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    )

    LOGO_SVG = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
        '<path d="M0 0h4v4H0z"/></svg>'
    )

    def setUp(self):
        if not hasattr(self, "assertRaisesRegex"):
            self.assertRaisesRegex = self.assertRaisesRegexp

        # Run each test from within a temporary directory, so any files
        # written by tests do not pollute the project directory.
        self._tempdir = tempfile.TemporaryDirectory(prefix="anybadge_test_")
        self.addCleanup(self._tempdir.cleanup)
        self._orig_cwd = os.getcwd()
        self.addCleanup(lambda: os.chdir(self._orig_cwd))
        os.chdir(self._tempdir.name)

        # Clear the logo memoization cache, so tests using mocked
        # downloads do not affect each other.
        logos._LOGO_CACHE.clear()

    def _write_logo_file(self, name="logo.svg", content=None):
        """Write a logo file (text) into the test directory."""
        with open(name, mode="w", encoding="utf-8") as file_handle:
            file_handle.write(content if content is not None else self.LOGO_SVG)
        return name

    def test_logo_bundled(self):
        """Test using a logo bundled with the package, with no network access."""
        plain = Badge("stars", "123")
        badge = Badge("stars", "123", logo="python")

        svg = badge.badge_svg_text
        self.assertIn("<image", svg)
        self.assertIn("data:image/svg+xml;base64,", svg)
        self.assertNotIn("{{ logo }}", svg)

        # The logo box adds edge margin + logo size + text gap, less the
        # single padding character it replaces.
        font_width = config.FONT_WIDTHS[config.DEFAULT_FONT][config.DEFAULT_FONT_SIZE]
        self.assertEqual(
            badge.badge_width,
            plain.badge_width
            + config.LOGO_MARGIN
            + config.LOGO_SIZE
            + config.LOGO_TEXT_GAP
            - int(config.NUM_PADDING_CHARS * font_width),
        )

    def test_logo_bundled_list(self):
        """Test that common project logos are bundled with the package."""
        builtin = logos.builtin_logos()
        for name in ("docker", "github", "gitlab", "python"):
            self.assertIn(name, builtin)

    def test_logo_local_file(self):
        """Test embedding a logo from a local SVG file."""
        logo_file = self._write_logo_file()

        badge = Badge("stars", "123", logo=logo_file)

        expected_uri = "data:image/svg+xml;base64,%s" % (
            base64.b64encode(self.LOGO_SVG.encode()).decode()
        )
        self.assertIn(expected_uri, badge.badge_svg_text)

    def test_logo_png_file(self):
        """Test embedding a logo from a local PNG file, with correct MIME type."""
        with open("logo.png", mode="wb") as file_handle:
            file_handle.write(base64.b64decode(self.PNG_BASE64))

        badge = Badge("stars", "123", logo="logo.png")

        self.assertIn("data:image/png;base64,", badge.badge_svg_text)

    def test_logo_position_left_and_right(self):
        """Test that left logos start at the margin, right logos end at the edge."""
        left = Badge("stars", "123", logo="python")
        right = Badge("stars", "123", logo="python", logo_position="right")

        expected_geometry = 'y="%s" width="%s" height="%s"' % (
            config.LOGO_Y,
            config.LOGO_SIZE,
            config.LOGO_SIZE,
        )

        self.assertIn(
            '<image x="%s" %s' % (config.LOGO_MARGIN, expected_geometry),
            left.badge_svg_text,
        )
        self.assertIn(
            '<image x="%s" %s'
            % (
                right.badge_width - config.LOGO_MARGIN - config.LOGO_SIZE,
                expected_geometry,
            ),
            right.badge_svg_text,
        )

    def test_logo_widths_and_anchors(self):
        """Test that the logo box is included in widths and shifts anchors."""
        plain = Badge("stars", "123")
        left = Badge("stars", "123", logo="python")
        right = Badge("stars", "123", logo="python", logo_position="right")
        # The logo replaces the single padding character on its side, in
        # exchange for edge margin, logo size and the text gap.
        font_width = config.FONT_WIDTHS[config.DEFAULT_FONT][config.DEFAULT_FONT_SIZE]
        single_pad = int(config.NUM_PADDING_CHARS * font_width)
        logo_box = (
            config.LOGO_MARGIN + config.LOGO_SIZE + config.LOGO_TEXT_GAP - single_pad
        )

        for badge in (left, right):
            self.assertEqual(badge.logo_box_width, logo_box)
            self.assertEqual(badge.badge_width, plain.badge_width + logo_box)

        # Label text shifts right when the logo is on the left. With the
        # logo on the right the color split moves left of the logo box, so
        # the value text box is unchanged and stays centered.
        self.assertEqual(
            left.label_anchor,
            left.color_split_position / 2 + logo_box / 2,
        )
        self.assertEqual(
            right.value_anchor,
            right.color_split_position + right.value_width / 2,
        )

        # The colored value area and value box only extend when the logo
        # is on the right.
        self.assertEqual(left.value_color_width, plain.value_color_width)
        self.assertEqual(right.value_color_width, plain.value_color_width + logo_box)
        self.assertEqual(right.value_box_width, plain.value_box_width + logo_box)

    def test_logo_text_gap(self):
        """Test the gap between the logo and the adjacent text on both sides."""
        left = Badge("stars", "123", logo="python")
        right = Badge("stars", "123", logo="python", logo_position="right")

        for badge in (left, right):
            svg = badge.badge_svg_text
            icon_x = float(svg.split('<image x="', 1)[1].split('"', 1)[0])
            icon_right = icon_x + config.LOGO_SIZE

            if badge is left:
                # Text starts within LOGO_TEXT_GAP of the icon's right edge.
                text_left = badge.label_anchor - badge.get_text_width("stars") / 2
                self.assertAlmostEqual(icon_right + config.LOGO_TEXT_GAP, text_left)
            else:
                # Value text ends within LOGO_TEXT_GAP of the icon's left edge.
                text_right = badge.value_anchor + badge.get_text_width("123") / 2
                self.assertAlmostEqual(text_right + config.LOGO_TEXT_GAP, icon_x)

    def test_logo_no_placeholder_in_output(self):
        """Test that the logo template placeholder is replaced, not left."""
        badge = Badge("stars", "123")

        self.assertNotIn("{{ logo }}", badge.badge_svg_text)
        self.assertNotIn("<image", badge.badge_svg_text)
        self.assertEqual(badge.logo_markup, "")

    def test_logo_invalid_position(self):
        """Test that an invalid logo position is rejected."""
        with self.assertRaisesRegex(ValueError, r'Invalid logo position "top"\.'):
            Badge("stars", "123", logo="python", logo_position="top")

    def test_logo_position_without_logo(self):
        """Test that logo_position requires a logo."""
        with self.assertRaisesRegex(
            ValueError, "A logo must be provided when a logo_position is specified"
        ):
            Badge("stars", "123", logo_position="right")

    def test_logo_search_dirs(self):
        """Test resolving a logo slug from a vendored logos directory."""
        os.mkdir("logos")
        self._write_logo_file(os.path.join("logos", "mysprite.svg"))

        badge = Badge("stars", "123", logo="mysprite", logo_dirs=["logos"])

        self.assertIn("data:image/svg+xml;base64,", badge.badge_svg_text)

    def test_logo_unknown_slug_raises_clean_error(self):
        """Test that a slug with no local match falls back to CDN download."""
        with mock.patch.object(
            logos, "_download", side_effect=ValueError("download failed")
        ) as mock_download:
            with self.assertRaisesRegex(ValueError, "download failed"):
                Badge("stars", "123", logo="no_such_slug_xyz")

        mock_download.assert_called_once()

    def test_logo_data_uri_passthrough(self):
        """Test that a data URI logo is used directly."""
        uri = "data:image/svg+xml;base64,%s" % (
            base64.b64encode(self.LOGO_SVG.encode()).decode()
        )
        badge = Badge("stars", "123", logo=uri)

        self.assertIn(uri, badge.badge_svg_text)

    def test_logo_repr(self):
        """Test that the repr can recreate a badge with a logo."""
        badge = Badge("stars", "123", logo="python", logo_position="right")

        recreated = eval(repr(badge))  # noqa: S307 - test-controlled input

        self.assertEqual(recreated.logo, badge.logo)
        self.assertEqual(recreated.logo_position, badge.logo_position)

    def test_logo_memoization(self):
        """Test that repeated badges with the same logo download only once."""
        with mock.patch.object(
            logos, "_download", return_value=self.LOGO_SVG.encode()
        ) as mock_download:
            _ = Badge("stars", "123", logo="not_a_bundled_slug")
            _ = Badge("stars", "456", logo="not_a_bundled_slug")

        mock_download.assert_called_once()

    def test_cli_badge_with_logo(self):
        """Test generating a badge with a logo from the command line."""
        retval = main(
            ["-l", "stars", "-v", "123", "--logo", "python", "--file", "out.svg"]
        )

        self.assertEqual(retval, 0)
        with open("out.svg", encoding="utf-8") as file_handle:
            svg = file_handle.read()
        self.assertIn("<image", svg)
        self.assertIn("data:image/svg+xml;base64,", svg)

    def test_cli_fetch_logos(self):
        """Test the fetch-logos mode writes vendored logo files."""
        with mock.patch.object(
            logos, "_download", return_value=self.LOGO_SVG.encode()
        ) as mock_download:
            retval = main(["fetch-logos", "mysprite", "mysprite2", "-d", "logos"])

        self.assertEqual(retval, 0)
        self.assertTrue(os.path.isfile("logos/mysprite.svg"))
        self.assertTrue(os.path.isfile("logos/mysprite2.svg"))
        self.assertEqual(mock_download.call_count, 2)

        # Running again should skip existing files without downloading.
        logos._LOGO_CACHE.clear()
        with mock.patch.object(logos, "_download") as mock_download:
            retval = main(["fetch-logos", "mysprite", "-d", "logos"])
            self.assertEqual(retval, 0)
            self.assertEqual(mock_download.call_count, 0)

        # With --force the file is downloaded again and overwritten.
        logos._LOGO_CACHE.clear()
        with mock.patch.object(
            logos, "_download", return_value=self.LOGO_SVG.encode()
        ) as mock_download:
            retval = main(["fetch-logos", "mysprite", "-d", "logos", "--force"])
            self.assertEqual(retval, 0)
            self.assertEqual(mock_download.call_count, 1)

    def test_cli_fetch_logos_download_error(self):
        """Test that a download failure results in a clean error."""
        with mock.patch.object(
            logos, "_download", side_effect=ValueError("network unreachable")
        ):
            retval = main(["fetch-logos", "not_a_bundled_slug"])

        self.assertEqual(retval, 1)
