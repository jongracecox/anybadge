from unittest import TestCase
from anybadge import Badge


class TestAnybadge(TestCase):
    """Test case class for anybadge package."""

    def test_badge_width_with_long_value_text(self):
        """Test the width of a badge generated with a long text value."""

        badge = Badge(label='CppCheck',
                      value='err: 2 | warn: 9 | info: 99 | style: 365',
                      default_color='red')

        badge.write_badge('test_badge_1.svg', overwrite=True)

        self.assertLessEqual(badge.badge_width, 326)

    def test_badge_width_with_long_value_text_zero_padding(self):
        """Test the width of a badge generated with a long text value."""

        badge = Badge(label='CppCheck',
                      value='err: 2 | warn: 9 | info: 99 | style: 365',
                      default_color='red',
                      num_padding_chars=0)

        badge.write_badge('test_badge_2.svg', overwrite=True)

        self.assertLessEqual(badge.badge_width, 306)

    def test_badge_width_with_medium_value_text(self):
        """Test the width of a badge generated with a medium text value."""

        badge = Badge(label='medium',
                      value='89.67%',
                      default_color='green')

        badge.write_badge('test_badge_3.svg', overwrite=True)

        self.assertLessEqual(badge.badge_width, 138)

    def test_badge_width_with_medium_value_text_zero_pad(self):
        """Test the width of a badge generated with a medium text value."""

        badge = Badge(label='medium',
                      value='89.67%',
                      default_color='green',
                      num_padding_chars=0)

        badge.write_badge('test_badge_4.svg', overwrite=True)

        self.assertLessEqual(badge.badge_width, 118)

    def test_badge_width_with_short_value_text(self):
        """Test the width of a badge generated with a short text value."""

        badge = Badge(label='short',
                      value='1',
                      default_color='green')

        badge.write_badge('test_badge_5.svg', overwrite=True)

        self.assertLessEqual(badge.badge_width, 101)

    def test_badge_width_with_short_value_text_zero_pad(self):
        """Test the width of a badge generated with a short text value."""

        badge = Badge(label='short',
                      value='1',
                      default_color='green',
                      num_padding_chars=0)

        badge.write_badge('test_badge_6.svg', overwrite=True)

        self.assertLessEqual(badge.badge_width, 81)

    def test_badge_width_with_tiny_value_text(self):
        """Test the width of a badge generated with a short text value."""

        badge = Badge(label='a',
                      value='1',
                      default_color='green')

        badge.write_badge('test_badge_7.svg', overwrite=True)

        self.assertLessEqual(badge.badge_width, 76)

    def test_badge_with_thresholds(self):
        """Test generating a badge using thresholds."""
        thresholds = {
            2: 'red', 4: 'orange', 6: 'green', 8: 'brightgreen'
        }

        badge = Badge('test', '2.22', value_suffix='%',
                      thresholds=thresholds)

        badge.write_badge('test_badge_8.svg', overwrite=True)

    def test_badge_with_text_color(self):
        """Test generating a badge with alternate text_color."""

        badge = Badge('test', '2.22', value_suffix='%',
                      text_color='#010101,#101010')

        badge.write_badge('test_badge_9.svg', overwrite=True)

    def test_multiple_badges_in_one_session(self):

        badges = [
            Badge('something', value='100', value_suffix='%', num_padding_chars=0),
            Badge('coverage', value='1234567890'),
        ]

        self.assertNotEqual(badges[0].badge_width, badges[1].badge_width)

    def test_multiple_badges_get_different_mask_id(self):
        badges = [
            Badge('something', value='100', value_suffix='%', num_padding_chars=0),
            Badge('coverage', value='1234567890'),
        ]

        self.assertNotEqual(badges[0].mask_id, badges[1].mask_id)

    def test_integer_value_is_handled_as_integer(self):
        badge = Badge('test', value='1234')

        self.assertTrue(badge.value_is_int)
        self.assertFalse(badge.value_is_float)

    def test_float_value_is_handled_as_float(self):
        badge = Badge('test', value='1234.1')

        self.assertFalse(badge.value_is_int)
        self.assertTrue(badge.value_is_float)

    def test_float_value_with_zero_decimal(self):
        badge = Badge('test', value='10.00')

        self.assertFalse(badge.value_is_int)
        self.assertTrue(badge.value_is_float)
        badge.write_badge('test_badge_10.svg', overwrite=True)

    def test_float_value_with_non_zero_decimal(self):
        badge = Badge('test', value='10.01')

        self.assertFalse(badge.value_is_int)
        self.assertTrue(badge.value_is_float)
        badge.write_badge('test_badge_11.svg', overwrite=True)
