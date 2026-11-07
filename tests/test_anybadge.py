import io
import os
import subprocess
import sys
import tempfile
from contextlib import redirect_stdout
from pathlib import Path
from unittest import TestCase, mock
from anybadge import Badge
from anybadge.cli import main, parse_args

TESTS_DIR = Path(__file__).parent
PROJECT_ROOT = TESTS_DIR.parent


class TestAnybadge(TestCase):
    """Test case class for anybadge package."""

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

    def test_badge_equal_label_value_width(self):
        """Test that label and value widths are equal when text is the same."""
        badge = Badge(label="a", value="a", num_padding_chars=0)

        self.assertEqual(badge.label_width, badge.value_width)

    @staticmethod
    def _has_emoji_package() -> bool:
        """Test helper indicating whether the optional emoji package is installed."""
        try:
            import emoji
        except ImportError:
            return False
        else:
            return True

    @staticmethod
    def make_badge_no_emoji_package(*args, **kwargs):
        """Create a Badge with a mocked ImportError for the emoji package.

        Setting sys.modules["emoji"] to None makes ``import emoji`` fail, the
        same as would happen when the package is not installed.
        """
        with mock.patch.dict(sys.modules, {"emoji": None}):
            return Badge(*args, **kwargs)

    def test_badge_emoji_shortcode_value(self):
        """Test that :emoji: shortcodes in the value are converted, or left as text without the emoji package."""
        badge_with = Badge(label="pipeline", value=":smile:")
        badge_without = self.make_badge_no_emoji_package(
            label="pipeline", value=":smile:"
        )

        if self._has_emoji_package():
            self.assertEqual(badge_with.value_text, "\U0001F604")
        else:
            self.assertEqual(badge_with.value_text, ":smile:")
        self.assertEqual(badge_without.value_text, ":smile:")

    def test_badge_emoji_shortcode_label(self):
        """Test that :emoji: shortcodes in the label are converted, or left as text without the emoji package."""
        badge_with = Badge(label=":rocket: deploy", value="123")
        badge_without = self.make_badge_no_emoji_package(
            label=":rocket: deploy", value="123"
        )

        if self._has_emoji_package():
            self.assertEqual(badge_with.label, "\U0001F680 deploy")
        else:
            self.assertEqual(badge_with.label, ":rocket: deploy")
        self.assertEqual(badge_without.label, ":rocket: deploy")

    def test_badge_emoji_shortcode_cldr_name(self):
        """Test that Unicode CLDR shortcode names are supported, or left as text without the emoji package."""
        badge_with = Badge(label="pipeline", value=":grinning_face:")
        badge_without = self.make_badge_no_emoji_package(
            label="pipeline", value=":grinning_face:"
        )

        if self._has_emoji_package():
            self.assertEqual(badge_with.value_text, "\U0001F600")
        else:
            self.assertEqual(badge_with.value_text, ":grinning_face:")
        self.assertEqual(badge_without.value_text, ":grinning_face:")

    def test_badge_emoji_shortcode_special_chars(self):
        """Test that GitHub-style aliases with + and _ characters are supported, or left as text without the emoji package."""
        badge_with = Badge(label=":+1:", value=":tada:")
        badge_without = self.make_badge_no_emoji_package(label=":+1:", value=":tada:")

        if self._has_emoji_package():
            self.assertEqual(badge_with.label, "\U0001F44D")
            self.assertEqual(badge_with.value_text, "\U0001F389")
        else:
            self.assertEqual(badge_with.label, ":+1:")
            self.assertEqual(badge_with.value_text, ":tada:")
        self.assertEqual(badge_without.label, ":+1:")
        self.assertEqual(badge_without.value_text, ":tada:")

    def test_badge_emoji_shortcode_value_prefix_suffix(self):
        """Test that :emoji: shortcodes in value prefix and suffix are converted, or left as text without the emoji package."""
        kwargs = {
            "label": "downloads",
            "value": "123",
            "value_prefix": ":+1:",
            "value_suffix": ":tada:",
        }
        badge_with = Badge(**kwargs)
        badge_without = self.make_badge_no_emoji_package(**kwargs)

        if self._has_emoji_package():
            self.assertEqual(badge_with.value_text, "\U0001F44D123\U0001F389")
        else:
            self.assertEqual(badge_with.value_text, ":+1:123:tada:")
        self.assertEqual(badge_without.value_text, ":+1:123:tada:")

    def test_badge_emoji_shortcode_width(self):
        """Test that shortcode text gets the same width as the resulting emoji."""
        if not self._has_emoji_package():
            self.skipTest("emoji package is not installed")

        badge_short = Badge(label="pipeline", value=":smile:")
        badge_emoji = Badge(label="pipeline", value="\U0001F604")

        self.assertEqual(badge_short.value_width, badge_emoji.value_width)
        self.assertEqual(badge_short.badge_width, badge_emoji.badge_width)

    def test_badge_emoji_shortcode_without_emoji_package(self):
        """Test that :emoji: shortcodes are left as text without the emoji package."""
        badge = self.make_badge_no_emoji_package(label="pipeline", value=":smile:")

        self.assertEqual(badge.label, "pipeline")
        self.assertEqual(badge.value_text, ":smile:")

    def test_badge_emoji_shortcode_value_thresholds_uses_raw_value(self):
        """Test that thresholds match against the original value text."""
        badge = Badge(
            label="pipeline",
            value=":smile:",
            thresholds={":smile:": "green", "failing": "red"},
        )

        self.assertEqual(badge.badge_color, "green")

    def test_badge_write_badge_with_emoji_is_utf8(self):
        """Test that badges containing emoji characters are written as UTF-8.

        This is a regression test for Windows, where the platform default
        encoding (cp1252) cannot represent emoji characters.
        """
        badge = Badge(label="pipeline", value="\U0001F604")

        badge.write_badge("test_badge_emoji.svg", overwrite=True)

        text = Path("test_badge_emoji.svg").read_text(encoding="utf-8")
        self.assertIn("\U0001F604", text)

    def test_badge_emoji_font_size_default(self):
        """Test that the default emoji font size is the font size plus 3."""
        badge = Badge(label="a", value="\U0001F604", font_size=11)

        self.assertEqual(badge.emoji_font_size, 14)

    def test_badge_emoji_font_size_from_arg(self):
        """Test that the emoji font size can be passed as an argument."""
        badge = Badge(label="a", value="\U0001F604", emoji_font_size=12)

        self.assertEqual(badge.emoji_font_size, 12)

    def test_badge_emoji_font_size_markup(self):
        """Test that emoji characters are wrapped in font-size tspans."""
        badge = Badge(label="\U0001F680 deploy", value="\U0001F604")

        self.assertEqual(badge.value_markup, '<tspan font-size="14">\U0001F604</tspan>')
        self.assertEqual(
            badge.label_markup,
            '<tspan font-size="14">\U0001F680</tspan> deploy',
        )
        # Non-emoji text is left alone
        self.assertEqual(Badge(label="a", value="123").value_markup, "123")

    def test_badge_emoji_font_size_markup_without_emoji_package(self):
        """Test that emoji markup is applied without the emoji package too."""
        badge = self.make_badge_no_emoji_package(
            label="\U0001F680 deploy", value="\U0001F604"
        )

        self.assertEqual(badge.value_markup, '<tspan font-size="14">\U0001F604</tspan>')

    def test_badge_emoji_font_size_markup_not_in_aria_label(self):
        """Test that the aria label contains plain emoji text, without tspans."""
        badge = Badge(label="pipeline", value="\U0001F604")

        self.assertEqual(badge.aria_label, "pipeline: \U0001F604")

    def test_badge_emoji_font_size_disabled(self):
        """Test that emoji are not wrapped when the emoji font size equals the font size."""
        badge = Badge(label="pipeline", value="\U0001F604", emoji_font_size=11)

        self.assertEqual(badge.value_markup, "\U0001F604")

    def test_badge_emoji_font_size_width(self):
        """Test that larger emoji font sizes are accounted for in badge width."""
        badge_scaled = Badge(label="a", value="\U0001F604", num_padding_chars=0)
        badge_unscaled = Badge(
            label="a", value="\U0001F604", num_padding_chars=0, emoji_font_size=11
        )

        self.assertGreater(badge_scaled.value_width, badge_unscaled.value_width)

    def test_cli_parse_args_emoji_font_size(self):
        """Test that --emoji-font-size is parsed and passed to the badge."""
        from anybadge.cli import parse_args

        parsed = parse_args(["--label", "a", "--value", "1", "--emoji-font-size", "12"])

        self.assertEqual(parsed.emoji_font_size, 12)

    def test_badge_equal_split(self):
        """Test that the color split is in the middle when label and value are equal width."""
        badge = Badge(label="a", value="a")

        self.assertEqual(int(badge.badge_width / 2), badge.color_split_position)

    def test_badge_equal_split_no_padding(self):
        """Test that the color split is in the middle when label and value are equal width."""
        badge = Badge(label="a", value="a", num_padding_chars=0)

        self.assertEqual(int(badge.badge_width / 2), badge.color_split_position)

    def test_badge_width_with_long_value_text(self):
        """Test the width of a badge generated with a long text value."""

        badge = Badge(
            label="CppCheck",
            value="err: 2 | warn: 9 | info: 99 | style: 365",
            default_color="red",
        )

        badge.write_badge("test_badge_1.svg", overwrite=True)

        self.assertLessEqual(badge.badge_width, 326)

    def test_badge_width_with_long_value_text_zero_padding(self):
        """Test the width of a badge generated with a long text value."""

        badge = Badge(
            label="CppCheck",
            value="err: 2 | warn: 9 | info: 99 | style: 365",
            default_color="red",
            num_padding_chars=0,
        )

        badge.write_badge("test_badge_2.svg", overwrite=True)

        self.assertLessEqual(badge.badge_width, 306)

    def test_badge_width_with_medium_value_text(self):
        """Test the width of a badge generated with a medium text value."""

        badge = Badge(label="medium", value="89.67%", default_color="green")

        badge.write_badge("test_badge_medium.svg", overwrite=True)

        self.assertLessEqual(badge.badge_width, 138)

    def test_badge_width_with_medium_value_text_zero_pad(self):
        """Test the width of a badge generated with a medium text value."""

        badge = Badge(
            label="medium no padding",
            value="89.67%",
            default_color="green",
            num_padding_chars=0,
        )

        badge.write_badge("test_badge_medium_no_padding.svg", overwrite=True)

        self.assertLessEqual(badge.badge_width, 156)

    def test_badge_width_with_short_value_text(self):
        """Test the width of a badge generated with a short text value."""

        badge = Badge(label="short", value="1", default_color="green")

        badge.write_badge("test_badge_short.svg", overwrite=True)

        self.assertLessEqual(badge.badge_width, 101)

    def test_badge_width_with_short_value_text_zero_pad(self):
        """Test the width of a badge generated with a short text value."""

        badge = Badge(
            label="short value no padding",
            value="1",
            default_color="green",
            num_padding_chars=0,
        )

        badge.write_badge("test_badge_short_no_padding.svg", overwrite=True)

        self.assertLessEqual(badge.badge_width, 143)

    def test_badge_width_with_tiny_value_text(self):
        """Test the width of a badge generated with a short text value."""

        badge = Badge(label="a", value="1", default_color="green")

        badge.write_badge("test_badge_tiny_text_value.svg", overwrite=True)

        self.assertLessEqual(badge.badge_width, 76)

    def test_badge_width_with_tiny_value_text_no_padding(self):
        """Test the width of a badge generated with a short text value."""

        badge = Badge(label="a", value="1", default_color="green", num_padding_chars=0)

        badge.write_badge("test_badge_tiny_text_value_no_padding.svg", overwrite=True)

        self.assertLessEqual(badge.badge_width, 76)

    def test_badge_with_thresholds(self):
        """Test generating a badge using thresholds."""
        thresholds = {2: "red", 4: "orange", 6: "green", 8: "brightgreen"}

        badge = Badge("thresholds", "2.22", value_suffix="%", thresholds=thresholds)

        badge.write_badge("test_badge_thresholds.svg", overwrite=True)

    def test_badge_with_text_color(self):
        """Test generating a badge with alternate text_color."""

        badge = Badge(
            "text color", "2.22", value_suffix="%", text_color="#010101,#101010"
        )

        badge.write_badge("test_badge_text_color.svg", overwrite=True)

    def test_multiple_badges_in_one_session(self):

        badges = [
            Badge("multiple 1", value="100", value_suffix="%", num_padding_chars=0),
            Badge("multiple 2", value="1234567890"),
        ]

        self.assertNotEqual(badges[0].badge_width, badges[1].badge_width)

    def test_multiple_badges_get_different_mask(self):
        badges = [
            Badge("multiple 1", value="100", value_suffix="%", num_padding_chars=0),
            Badge("multiple 2", value="1234567890"),
        ]

        self.assertNotEqual(badges[0].mask_str, badges[1].mask_str)

    def test_integer_str_value_is_handled_as_integer(self):
        badge = Badge("integer", value="1234")

        self.assertTrue(badge.value_is_int)
        self.assertFalse(badge.value_is_float)
        badge.write_badge("test_badge_int_str.svg", overwrite=True)

    def test_integer_int_value_is_handled_as_integer(self):
        badge = Badge("integer", value=1234)

        self.assertTrue(badge.value_is_int)
        self.assertFalse(badge.value_is_float)
        badge.write_badge("test_badge_int.svg", overwrite=True)

    def test_float_str_value_is_handled_as_float(self):
        badge = Badge("float str", value="1234.1")

        self.assertFalse(badge.value_is_int)
        self.assertTrue(badge.value_is_float)
        badge.write_badge("test_badge_float_str.svg", overwrite=True)

    def test_float_value_is_handled_as_float(self):
        badge = Badge("float int", value=1234.1)

        self.assertFalse(badge.value_is_int)
        self.assertTrue(badge.value_is_float)
        badge.write_badge("test_badge_float.svg", overwrite=True)

    def test_float_value_with_zero_decimal(self):
        badge = Badge("float with zeros", value="10.00")

        self.assertFalse(badge.value_is_int)
        self.assertTrue(badge.value_is_float)
        badge.write_badge("test_badge_float_zeros.svg", overwrite=True)

    def test_float_value_with_non_zero_decimal(self):
        badge = Badge("float str no decimal", value="10.01")

        self.assertFalse(badge.value_is_int)
        self.assertTrue(badge.value_is_float)
        badge.write_badge("test_badge_float-str-no-decimal.svg", overwrite=True)

    def test_padding_label(self):
        badge = Badge("label padding", value="10.01", num_label_padding_chars=2)

        badge.write_badge("test_badge_padding_label.svg", overwrite=True)

    def test_padding_value(self):
        badge = Badge("value padding", value="10.01", num_value_padding_chars=2)

        badge.write_badge("test_badge_padding_value.svg", overwrite=True)

    def test_value_formatting(self):
        badge = Badge("value formatting", value="10", value_format="%s hits/sec")

        self.assertEqual("10 hits/sec", badge.value_text)

    def test_font_name(self):
        font = "Arial, Helvetica, sans-serif"
        badge = Badge("font", value=font, font_name=font)
        badge.write_badge("test_badge_font.svg", overwrite=True)

        badge_repr = repr(badge)
        self.assertTrue("font_name='Arial, Helvetica, sans-serif'" in badge_repr)

    def test_invalid_font_name(self):
        font = "Invalid font"
        with self.assertRaises(ValueError):
            _ = Badge("font", value=font, font_name=font)

    def test_font_size(self):
        for size in [10, 11, 12]:
            badge = Badge("font size", value=size, font_size=size)
            badge.write_badge("test_badge_font_size_%s.svg" % size, overwrite=True)

    def test_font_size_repr(self):
        badge = Badge("font size", value=10, font_size=10)
        badge_repr = repr(badge)
        self.assertTrue("font_size=10" in badge_repr)

    def test_template_from_file(self):
        file = Path(__file__).parent / Path("template.svg")
        badge = Badge("template from file", value=file, template=file)
        _ = badge.badge_svg_text

    def test_repr_svg(self):
        badge = Badge("label", "value")
        self.assertEqual(badge.badge_svg_text, badge._repr_svg_())

    def test_accessibility_attributes_default_template(self):
        """Test that the default template exposes an accessible name."""
        badge = Badge("coverage", "97%")
        svg = badge.badge_svg_text

        self.assertIn('role="img"', svg)
        self.assertIn('aria-label="coverage: 97%"', svg)
        self.assertIn("<title>coverage: 97%</title>", svg)
        # <title> must be the first child of <svg>
        self.assertLess(svg.index("<title>"), svg.index("<linearGradient"))

    def test_accessibility_attributes_gitlab_scoped_template(self):
        """Test that the gitlab_scoped template exposes an accessible name."""
        badge = Badge("coverage", "97%", style="gitlab-scoped")
        svg = badge.badge_svg_text

        self.assertIn('role="img"', svg)
        self.assertIn('aria-label="coverage: 97%"', svg)
        self.assertIn("<title>coverage: 97%</title>", svg)
        self.assertLess(svg.index("<title>"), svg.index("<linearGradient"))

    def test_accessibility_attributes_escaped_text(self):
        """Test that label/value are escaped in the accessibility attributes."""
        badge = Badge('label <with> "quotes"', "1 < 2")
        svg = badge.badge_svg_text

        self.assertIn(
            "<title>label &lt;with&gt; &quot;quotes&quot;: 1 &lt; 2</title>", svg
        )
        self.assertIn(
            'aria-label="label &lt;with&gt; &quot;quotes&quot;: 1 &lt; 2"', svg
        )

    def test_accessibility_attributes_with_empty_text(self):
        """Test that aria-label omits empty label or value and their separator."""
        value_only = Badge("", "Value only").badge_svg_text
        label_only = Badge("Label only", "").badge_svg_text

        self.assertIn('aria-label="Value only"', value_only)
        self.assertIn("<title>Value only</title>", value_only)
        self.assertIn('aria-label="Label only"', label_only)
        self.assertIn("<title>Label only</title>", label_only)

    def test_str_value_with_threshold_and_default(self):
        badge = Badge(
            "label",
            value="fred",
            thresholds={"pass": "green", "fail": "red"},
            default_color="orange",
        )
        self.assertEqual("orange", badge.badge_color)

    def test_invalid_color(self):
        with self.assertRaises(ValueError):
            badge = Badge("label", value="fred", default_color="floberry")
            _ = badge.badge_color_code

    def test_invalid_color_message(self):
        """Test that the invalid color error names the bad color and lists valid options."""
        badge = Badge("label", value="fred", default_color="floberry")
        with self.assertRaisesRegex(
            ValueError,
            r'Invalid color code "floberry". Valid color codes are: .*MEDIUMBLUE',
        ):
            _ = badge.badge_color_code

    def test_cli_invalid_color_reports_error_without_traceback(self):
        """Test that an invalid color produces a single ERROR line and exit code 1."""
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            retval = main(
                ["--label", "label", "--value", "value", "--color", "floberry"]
            )

        self.assertEqual(1, retval)
        lines = stdout.getvalue().strip().splitlines()
        self.assertEqual(1, len(lines))
        self.assertTrue(lines[0].startswith("ERROR:"))
        self.assertIn('Invalid color code "floberry"', lines[0])
        self.assertIn("Valid color codes", lines[0])

    def test_cli_bad_threshold_reports_error_without_traceback(self):
        """Test that a malformed threshold produces a single ERROR line and exit code 1."""
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            retval = main(["--label", "label", "--value", "value", "2red"])

        self.assertEqual(1, retval)
        lines = stdout.getvalue().strip().splitlines()
        self.assertEqual(1, len(lines))
        self.assertTrue(lines[0].startswith("ERROR:"))
        self.assertIn("2red", lines[0])

    def test_cli_missing_font_reports_error(self):
        """Test that an unknown font produces exit code 1 and an ERROR line."""
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            retval = main(["--label", "label", "--value", "value", "--font", "BadFont"])

        self.assertEqual(1, retval)
        lines = stdout.getvalue().strip().splitlines()
        self.assertEqual(1, len(lines))
        self.assertTrue(lines[0].startswith("ERROR:"))
        self.assertIn("BadFont", lines[0])

    def test_cli_missing_template_reports_error(self):
        """Test that a missing template file produces exit code 1 and an ERROR line."""
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            retval = main(
                [
                    "--label",
                    "label",
                    "--value",
                    "value",
                    "--template",
                    "no_such_template.svg",
                ]
            )

        self.assertEqual(1, retval)
        self.assertTrue(stdout.getvalue().strip().startswith("ERROR:"))

    def test_cli_empty_args_does_not_read_sys_argv(self):
        """Test that main([]) does not fall back to reading sys.argv."""
        # Patch sys.argv with a bogus flag; argparse would SystemExit if it
        # were consumed, so falling through proves [] was honoured.
        with mock.patch.object(sys, "argv", ["anybadge", "--bogus-flag"]):
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                retval = main([])

        self.assertEqual(1, retval)
        self.assertTrue(stdout.getvalue().strip().startswith("ERROR:"))

    def test_module_exits_1_on_user_error(self):
        """Test that `python -m anybadge` exits with code 1 and no traceback."""
        process = subprocess.run(
            [
                sys.executable,
                "-m",
                "anybadge",
                "--label",
                "label",
                "--value",
                "value",
                "--color",
                "floberry",
            ],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
        )

        self.assertEqual(1, process.returncode)
        self.assertNotIn("Traceback", process.stderr)
        self.assertIn("ERROR:", process.stdout)

    def test_invalid_write_path(self):
        cwd = Path(os.getcwd())
        badge = Badge("label", "value")
        with self.assertRaisesRegex(
            ValueError, r"File location may not be a directory\."
        ):
            badge.write_badge("somedir/")

        with self.assertRaisesRegex(
            RuntimeError, r'File ".*exists\.svg" already exists\.'
        ):
            badge.write_badge(cwd / "exists")
            badge.write_badge(cwd / "exists")

        with self.assertRaisesRegex(
            RuntimeError, r'File ".*exists\.svg" already exists\.'
        ):
            badge.write_badge(str(cwd / "exists"))
            badge.write_badge(str(cwd / "exists"))

    def test_arg_parsing(self):
        args = parse_args(["-l", "label", "-v", "value"])
        self.assertEqual("label", args.label)
        self.assertEqual("value", args.value)

    def test_main_print(self):
        main(["--label", "label", "--value", "value"])

    def test_main_write_to_file(self):
        main(
            [
                "--label",
                "label",
                "--value",
                "value",
                "--file",
                "test_badge_main.svg",
                "--overwrite",
            ]
        )

    def test_main_thresholds(self):
        main(
            [
                "--label",
                "label",
                "--value",
                "value",
                "--file",
                "test_badge_main_threshold.svg",
                "--overwrite",
                "2=red",
                "4=orange",
            ]
        )

    def test_named_threshold(self):
        main(
            [
                "--value",
                "value",
                "--file",
                "test_badge_main_named_threshold.svg",
                "--overwrite",
                "coverage",
            ]
        )

    def test_version_comparison(self):
        # Define thresholds: <3.0.0=red, <3.2.0=orange <999.0.0=green
        badge = Badge(
            "Version",
            value="1.0.0",
            thresholds={"3.0.0": "red", "3.2.0": "orange", "999.0.0": "green"},
            semver=True,
        )
        self.assertEqual("red", badge.badge_color)

        # Define thresholds: <3.0.0=red, <3.2.0=orange <999.0.0=green
        badge = Badge(
            "Version",
            value="3.0.0",
            thresholds={"3.0.0": "red", "3.2.0": "orange", "999.0.0": "green"},
            semver=True,
        )
        self.assertEqual("orange", badge.badge_color)

        # Define thresholds: <3.0.0=red, <3.2.0=orange <999.0.0=green
        badge = Badge(
            "Version",
            value="3.1.0",
            thresholds={"3.0.0": "red", "3.2.0": "orange", "999.0.0": "green"},
            semver=True,
        )
        self.assertEqual("orange", badge.badge_color)

        # Define thresholds: <3.0.0=red, <3.2.0=orange <999.0.0=green
        badge = Badge(
            "Version",
            value="3.2.0",
            thresholds={"3.0.0": "red", "3.2.0": "orange", "999.0.0": "green"},
            semver=True,
        )
        self.assertEqual("green", badge.badge_color)

        badge = Badge(
            "Version",
            value="3.2.1",
            thresholds={"3.0.0": "red", "3.2.0": "orange", "999.0.0": "green"},
            semver=True,
        )
        self.assertEqual("green", badge.badge_color)

        # Define thresholds: <3.0.0=red, <3.2.0=orange <999.0.0=green
        badge = Badge(
            "Version",
            value="10.20.30",
            thresholds={"3.0.0": "red", "3.2.0": "orange", "999.0.0": "green"},
            semver=True,
        )
        self.assertEqual("green", badge.badge_color)

        # Define thresholds: <3.0.0=red, <13.2.0=orange <999.0.0=green
        badge = Badge(
            "Version",
            value="14.0.0",
            thresholds={"3.0.0": "red", "13.2.0": "orange", "999.0.0": "green"},
            semver=True,
        )
        self.assertEqual("green", badge.badge_color)

        badge = Badge(
            "Version",
            value="12.0.0",
            thresholds={"3.0.0": "red", "13.2.0": "orange", "999.0.0": "green"},
            semver=True,
        )
        self.assertEqual("orange", badge.badge_color)

    def test_module_same_output_as_main_cli(self):
        """Test that `python -m anybadge` is equivalent to calling `anybadge` directly."""

        output_module = subprocess.check_output(
            [sys.executable, "-m", "anybadge", "--help"],
            cwd=str(PROJECT_ROOT),
        )

        script_name = "anybadge.exe" if os.name == "nt" else "anybadge"
        anybadge_executable = Path(sys.executable).parent / script_name
        if not anybadge_executable.exists():
            self.skipTest("anybadge console script is not installed")

        output_script = subprocess.check_output([str(anybadge_executable), "--help"])

        self.assertEqual(output_module, output_script)

    def test_badge_with_no_label(self):
        """Test the dimensions for a badge with no label."""
        badge = Badge(
            label="",
            value="Value",
        )
        self.assertEqual(
            badge.label_width,
            0,
            "Expected label width to be 0 for badge with no label.",
        )

    def test_badge_with_no_value(self):
        """Test the dimensions for a badge with no value."""
        badge = Badge(
            label="Label",
            value="",
        )
        self.assertEqual(
            badge.value_width,
            0,
            "Expected value width to be 0 for badge with no value.",
        )

    def test_badge_with_no_label_and_no_value(self):
        """Test that an exception is raised when trying to create a badge with no label or value."""
        with self.assertRaisesRegex(
            ValueError, r"Either a label or a value must be provided for a badge\."
        ):
            _ = Badge(
                label="",
                value="",
            )

        with self.assertRaisesRegex(
            ValueError, r"Either a label or a value must be provided for a badge\."
        ):
            _ = Badge(
                label=None,
                value=None,
            )

    def test_badge_default_escaping(self):
        """Test explicitly using value and label escaping for the badge."""
        badge = Badge(
            label="My > Label",
            value="My > Value",
        )
        self.assertEqual(badge.encoded_label, "My &gt; Label")
        self.assertEqual(badge.encoded_value, "My &gt; Value")

    def test_badge_explicit_escaping(self):
        """Test explicitly using value and label escaping for the badge."""
        badge = Badge(
            label="My > Label",
            value="My > Value",
            escape_label=True,
            escape_value=True,
        )
        self.assertEqual(badge.encoded_label, "My &gt; Label")
        self.assertEqual(badge.encoded_value, "My &gt; Value")

    def test_badge_without_escaping(self):
        """Test switching off value and label escaping for the badge."""
        badge = Badge(
            label="My > Label",
            value="My > Value",
            escape_label=False,
            escape_value=False,
        )
        self.assertEqual(badge.encoded_label, "My > Label")
        self.assertEqual(badge.encoded_value, "My > Value")
