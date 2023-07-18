import subprocess
from pathlib import Path
from unittest import TestCase
from anybadge import Badge
from anybadge.cli import main, parse_args


TESTS_DIR = Path(__file__).parent


class TestAnybadge(TestCase):
    """Test case class for anybadge package."""

    def setUp(self):
        if not hasattr(self, "assertRaisesRegex"):
            self.assertRaisesRegex = self.assertRaisesRegexp

    def test_badge_equal_label_value_width(self):
        """Test that label and value widths are equal when text is the same."""
        badge = Badge(label="a", value="a", num_padding_chars=0)

        self.assertEqual(badge.label_width, badge.value_width)

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

    def test_invalid_write_path(self):
        badge = Badge("label", "value")
        with self.assertRaisesRegex(
            ValueError, r"File location may not be a directory\."
        ):
            badge.write_badge("tests/")

        with self.assertRaisesRegex(
            RuntimeError, r'File ".*tests\/exists\.svg" already exists\.'
        ):
            badge.write_badge(TESTS_DIR / Path("exists"))
            badge.write_badge(TESTS_DIR / Path("exists"))

        with self.assertRaisesRegex(
            RuntimeError, r'File ".*tests\/exists\.svg" already exists\.'
        ):
            badge.write_badge(str(TESTS_DIR / Path("exists")))
            badge.write_badge(str(TESTS_DIR / Path("exists")))

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
        output_module = subprocess.check_output(["python", "-m", "anybadge", "--help"])
        output_script = subprocess.check_output(["anybadge", "--help"])
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
