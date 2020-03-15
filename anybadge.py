#!/usr/bin/python
"""
anybadge

A Python module for generating badges for your projects, with a focus on
simplicity and flexibility.
"""
import sys
import os
import re
import argparse
import textwrap

# Package information
version = __version__ = "0.0.0"
__version_info__ = tuple(re.split('[.-]', __version__))
__title__ = "anybadge"
__summary__ = "A simple, flexible badge generator."
__uri__ = "https://github.com/jongracecox/anybadge"


# Set some defaults
DEFAULT_FONT = 'DejaVu Sans,Verdana,Geneva,sans-serif'
DEFAULT_FONT_SIZE = 11
NUM_PADDING_CHARS = 0.5
DEFAULT_COLOR = '#4c1'
DEFAULT_TEXT_COLOR = '#fff'
MASK_ID_PREFIX = 'anybadge_'

# Dictionary for looking up approx pixel widths of
# supported fonts and font sizes.
FONT_WIDTHS = {
    'DejaVu Sans,Verdana,Geneva,sans-serif': {
        10: 9,
        11: 10,
        12: 11,
    },
    'Arial, Helvetica, sans-serif': {
        11: 8,
    },
}

# Create a dictionary of colors to make selections
# easier.
COLORS = {
    'white': '#FFFFFF',
    'silver': '#C0C0C0',
    'gray': '#808080',
    'black': '#000000',
    'red': '#e05d44',
    'brightred': '#FF0000',
    'maroon': '#800000',
    'olive': '#808000',
    'lime': '#00FF00',
    'brightyellow': '#FFFF00',
    'yellow': '#dfb317',
    'green': '#4c1',
    'yellowgreen': '#a4a61d',
    'aqua': '#00FFFF',
    'teal': '#008080',
    'blue': '#0000FF',
    'navy': '#000080',
    'fuchsia': '#FF00FF',
    'purple': '#800080',
    'orange': '#fe7d37',
    'lightgrey': '#9f9f9f',
}

# Template SVG with placeholders for various items that
# will be added during final creation.
TEMPLATE_SVG = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{{ badge width }}" height="20">
    <linearGradient id="b" x2="0" y2="100%">
        <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
        <stop offset="1" stop-opacity=".1"/>
    </linearGradient>
    <mask id="{{ mask id }}">
        <rect width="{{ badge width }}" height="20" rx="3" fill="#fff"/>
    </mask>
    <g mask="url(#{{ mask id }})">
        <path fill="#555" d="M0 0h{{ color split x }}v20H0z"/>
        <path fill="{{ color }}" d="M{{ color split x }} 0h{{ value width }}v20H{{ color split x }}z"/>
        <path fill="url(#b)" d="M0 0h{{ badge width }}v20H0z"/>
    </g>
    <g fill="{{ label text color }}" text-anchor="middle" font-family="{{ font name }}" font-size="{{ font size }}">
        <text x="{{ label anchor shadow }}" y="15" fill="#010101" fill-opacity=".3">{{ label }}</text>
        <text x="{{ label anchor }}" y="14">{{ label }}</text>
    </g>
    <g fill="{{ value text color }}" text-anchor="middle" font-family="{{ font name }}" font-size="{{ font size }}">
        <text x="{{ value anchor shadow }}" y="15" fill="#010101" fill-opacity=".3">{{ value }}</text>
        <text x="{{ value anchor }}" y="14">{{ value }}</text>
    </g>
</svg>"""

# Define some templates that can be used for common badge types, saving
# from having to provide thresholds and labels each time.
BADGE_TEMPLATES = {
    'pylint': {
        'threshold': '2=red 4=orange 8=yellow 10=green',
        'label': 'pylint'
    },
    'coverage': {
        'threshold': '50=red 60=orange 80=yellow 100=green',
        'label': 'coverage',
        'suffix': '%'
    }
}


class Badge(object):
    """
    Badge class used to generate badges.

    Args:
        label(str): Badge label text.
        value(str): Badge value text.
        font_name(str, optional): Name of font to use.
        font_size(int, optional): Font size.
        num_padding_chars(float, optional): Number of padding characters to use to give extra
            space around text.
        num_label_padding_chars(float, optional): Number of padding characters to use to give extra
            space around label text.
        num_value_padding_chars(float, optional): Number of padding characters to use to give extra
            space around value text.
        template(str, optional): String containing the SVG template.  This should be valid SVG
            file content with place holders for variables to be populated during rendering.
        value_prefix(str, optional): Prefix to be placed before value.
        value_suffix(str, optional): Suffix to be placed after value.
        thresholds(dict, optional): A dictionary containing thresholds used to select badge
            color based on the badge value.
        default_color(str, optional): Badge color as a name or as an HTML color code.
        use_max_when_value_exceeds(bool, optional): Choose whether to use the maximum threshold
            value when the badge value exceeds the top threshold.  Default is True.
        value_format(str, optional) String with formatting to be used to format the value text.
        text_color(str, optional): Text color as a name or as an HTML color code.

    Examples:

        Create a simple green badge:

        >>> badge = Badge('label', 123, default_color='green')

        Write a badge to file, overwriting any existing file:

        >>> badge = Badge('label', 123, default_color='green')
        >>> badge.write_badge('demo.svg', overwrite=True)

        Here are a number of examples showing thresholds, since there
        are certain situations that may not be obvious:

        >>> badge = Badge('pipeline', 'passing', thresholds={'passing': 'green', 'failing': 'red'})
        >>> badge.badge_color
        'green'

        2.32 is not <2
        2.32 is < 4, so 2.32 yields orange
        >>> badge = Badge('pylint', 2.32, thresholds={2: 'red',
        ...                                           4: 'orange',
        ...                                           8: 'yellow',
        ...                                           10: 'green'})
        >>> badge.badge_color
        'orange'

        8 is not <8
        8 is <4, so 8 yields orange
        >>> badge = Badge('pylint', 8, thresholds={2: 'red',
        ...                                        4: 'orange',
        ...                                        8: 'yellow',
        ...                                        10: 'green'})
        >>> badge.badge_color
        'green'

        10 is not <8, but use_max_when_value_exceeds defaults to
        True, so 10 yields green
        >>> badge = Badge('pylint', 11, thresholds={2: 'red',
        ...                                         4: 'orange',
        ...                                         8: 'yellow',
        ...                                         10: 'green'})
        >>> badge.badge_color
        'green'

        11 is not <10, and use_max_when_value_exceeds is set to
        False, so 11 yields the default color '#4c1'
        >>> badge = Badge('pylint', 11, use_max_when_value_exceeds=False,
        ...               thresholds={2: 'red', 4: 'orange', 8: 'yellow',
        ...                           10: 'green'})
        >>> badge.badge_color
        '#4c1'
    """

    def __init__(self, label, value, font_name=None, font_size=None,
                 num_padding_chars=None, num_label_padding_chars=None,
                 num_value_padding_chars=None, template=None,
                 value_prefix='', value_suffix='', thresholds=None, default_color=None,
                 use_max_when_value_exceeds=True, value_format=None, text_color=None):
        """Constructor for Badge class."""
        # Set defaults if values were not passed
        if not font_name:
            font_name = DEFAULT_FONT
        if not font_size:
            font_size = DEFAULT_FONT_SIZE
        if num_label_padding_chars is None:
            if num_padding_chars is None:
                num_label_padding_chars = NUM_PADDING_CHARS
            else:
                num_label_padding_chars = num_padding_chars
        if num_value_padding_chars is None:
            if num_padding_chars is None:
                num_value_padding_chars = NUM_PADDING_CHARS
            else:
                num_value_padding_chars = num_padding_chars
        if not template:
            template = TEMPLATE_SVG
        if not default_color:
            default_color = DEFAULT_COLOR
        if not text_color:
            text_color = DEFAULT_TEXT_COLOR

        self.label = label
        self.value = value
        self.value_format = value_format
        if value_format:
            value_text = str(value_format % self.value_type(value))
        else:
            value_text = str(self.value_type(value))
        self.value_prefix = value_prefix
        self.value_suffix = value_suffix
        self.value_text = value_prefix + value_text + value_suffix

        if font_name not in FONT_WIDTHS:
            raise ValueError('Font name "%s" not found. Available fonts: %s' % (font_name, ', '.join(FONT_WIDTHS.keys())))
        self.font_name = font_name
        self.font_size = font_size
        self.num_label_padding_chars = num_label_padding_chars
        self.num_value_padding_chars = num_value_padding_chars
        self.template = template
        self.thresholds = thresholds
        self.default_color = default_color

        # text_color can be passed as a single value or a pair of comma delimited values
        self.text_color = text_color
        text_colors = text_color.split(',')
        self.label_text_color = text_colors[0]
        self.value_text_color = text_colors[0]
        if len(text_colors) > 1:
            self.value_text_color = text_colors[1]

        self.use_max_when_value_exceeds = use_max_when_value_exceeds
        self.mask_id = self.__class__._get_next_mask_id()

    def __repr__(self):
        """Return a representation of the Badge object instance.

        The output of the __repr__ function could be used to recreate the current object.

        Examples:

            >>> badge = Badge('example', '123.456')
            >>> repr(badge)
            "Badge('example', '123.456')"

            >>> badge = Badge('example', '123.456', value_suffix='TB')
            >>> repr(badge)
            "Badge('example', '123.456', value_suffix='TB')"

            >>> badge = Badge('example', '123.456', text_color='#111111', value_suffix='TB')
            >>> repr(badge)
            "Badge('example', '123.456', value_suffix='TB', text_color='#111111')"

            >>> badge = Badge('example', '123', num_padding_chars=5)
            >>> repr(badge)
            "Badge('example', '123', num_padding_chars=5)"

            >>> badge = Badge('example', '123', num_label_padding_chars=5)
            >>> repr(badge)
            "Badge('example', '123', num_label_padding_chars=5)"

            >>> badge = Badge('example', '123', num_label_padding_chars=5, num_value_padding_chars=6,
            ...               template='template.svg', value_prefix='$', thresholds={10: 'green', 30: 'red'},
            ...               default_color='red', use_max_when_value_exceeds=False, value_format="%s m/s")
            >>> repr(badge)
            "Badge('example', '123', num_label_padding_chars=5, num_value_padding_chars=6, template='template.svg', value_prefix='$', thresholds={10: 'green', 30: 'red'}, default_color='red', use_max_when_value_exceeds=False, value_format='%s m/s')"

        """
        optional_args = ""
        if self.font_name != DEFAULT_FONT:
            optional_args += ", font_name=%s" % repr(self.font_name)
        if self.font_size != DEFAULT_FONT_SIZE:
            optional_args += ", font_size=%s" % repr(self.font_size)
        if self.num_label_padding_chars == self.num_value_padding_chars:
            if self.num_label_padding_chars != NUM_PADDING_CHARS:
                optional_args += ", num_padding_chars=%s" % repr(self.num_label_padding_chars)
        else:
            if self.num_label_padding_chars != NUM_PADDING_CHARS:
                optional_args += ", num_label_padding_chars=%s" % repr(self.num_label_padding_chars)
            if self.num_value_padding_chars != NUM_PADDING_CHARS:
                optional_args += ", num_value_padding_chars=%s" % repr(self.num_value_padding_chars)
        if self.template != TEMPLATE_SVG:
            optional_args += ", template=%s" % repr(self.template)
        if self.value_prefix != '':
            optional_args += ", value_prefix=%s" % repr(self.value_prefix)
        if self.value_suffix != '':
            optional_args += ", value_suffix=%s" % repr(self.value_suffix)
        if self.thresholds:
            optional_args += ", thresholds=%s" % repr(self.thresholds)
        if self.default_color != DEFAULT_COLOR:
            optional_args += ", default_color=%s" % repr(self.default_color)
        if not self.use_max_when_value_exceeds:
            optional_args += ", use_max_when_value_exceeds=%s" % repr(self.use_max_when_value_exceeds)
        if self.value_format:
            optional_args += ", value_format=%s" % repr(self.value_format)
        if self.text_color != DEFAULT_TEXT_COLOR:
            optional_args += ", text_color=%s" % repr(self.text_color)

        return "%s(%s, %s%s)" % (
            self.__class__.__name__,
            repr(self.label),
            repr(self.value),
            optional_args
        )

    def _repr_svg_(self):
        """Return SVG representation when used inside Jupyter notebook cells.
        
        This will render the SVG immediately inside a notebook cell when creating
        a Badge instance without assigning it to an identifier.
        """
        return self.badge_svg_text
    
    
    @classmethod
    def _get_next_mask_id(cls):
        """Return a new mask ID from a singleton sequence maintained on the class.

        Returns: str
        """
        if not hasattr(cls, 'mask_id'):
            cls.mask_id = 0

        cls.mask_id += 1

        return MASK_ID_PREFIX + str(cls.mask_id)

    @property
    def value_is_float(self):
        """Identify whether the value text is a float.

        Returns: bool
        """

        # If the value is an int then it should not be considered a float.
        # We need to check this first before we check whether it is a float because the
        # float check also returns True for an int string.
        if self.value_is_int:
            return False

        try:
            _ = float(self.value)
        except ValueError:
            return False
        else:
            return True

    @property
    def value_is_int(self):
        """Identify whether the value text is an int.

        Returns: bool
        """
        try:
            a = float(self.value)
            b = int(self.value)
        except ValueError:
            return False
        else:
            return a == b

    @property
    def value_type(self):
        """The Python type associated with the value.

        Returns: type
        """
        if self.value_is_float:
            return float
        elif self.value_is_int:
            return int
        else:
            return str

    @property
    def label_width(self):
        """The SVG width of the label text.

        Returns: int
        """
        return int(self.get_text_width(str(self.label)) + (2.0 * self.num_label_padding_chars * self.font_width))

    @property
    def value_width(self):
        """The SVG width of the value text.

        Returns: int
        """
        return int(self.get_text_width(str(self.value_text)) + (2.0 * self.num_value_padding_chars * self.font_width))

    @property
    def font_width(self):
        """Return the width multiplier for a font.

        Returns:
            int: Maximum pixel width of badges selected font.

        Example:

            >>> Badge(label='x', value='1').font_width
            10
        """
        return FONT_WIDTHS[self.font_name][self.font_size]

    @property
    def color_split_position(self):
        """The SVG x position where the color split should occur.

        Returns: int
        """
        return self.badge_width - self.value_width

    @property
    def label_anchor(self):
        """The SVG x position of the middle anchor for the label text.

        Returns: float
        """
        return self.color_split_position / 2

    @property
    def value_anchor(self):
        """The SVG x position of the middle anchor for the value text.

        Returns: float
        """
        return self.color_split_position + ((self.badge_width - self.color_split_position) / 2)

    @property
    def label_anchor_shadow(self):
        """The SVG x position of the label shadow anchor.

        Returns: float
        """
        return self.label_anchor + 1

    @property
    def value_anchor_shadow(self):
        """The SVG x position of the value shadow anchor.

        Returns: float
        """
        return self.value_anchor + 1

    @property
    def badge_width(self):
        """The total width of badge.

        Returns: int

        Examples:

            >>> badge = Badge('pylint', '5')
            >>> badge.badge_width
            61
        """
        return self.label_width + self.value_width

    @property
    def badge_svg_text(self):
        """The badge SVG text.

        Returns: str
        """

        # Identify whether template is a file or the actual template text
        if len(self.template.split('\n')) == 1:
            with open(self.template, mode='r') as file_handle:
                badge_text = file_handle.read()
        else:
            badge_text = self.template

        return badge_text.replace('{{ badge width }}', str(self.badge_width)) \
            .replace('{{ font name }}', self.font_name) \
            .replace('{{ font size }}', str(self.font_size)) \
            .replace('{{ label }}', self.label) \
            .replace('{{ value }}', self.value_text) \
            .replace('{{ label anchor }}', str(self.label_anchor)) \
            .replace('{{ label anchor shadow }}', str(self.label_anchor_shadow)) \
            .replace('{{ value anchor }}', str(self.value_anchor)) \
            .replace('{{ value anchor shadow }}', str(self.value_anchor_shadow)) \
            .replace('{{ color }}', self.badge_color_code) \
            .replace('{{ label text color }}', self.label_text_color) \
            .replace('{{ value text color }}', self.value_text_color) \
            .replace('{{ color split x }}', str(self.color_split_position)) \
            .replace('{{ value width }}', str(self.value_width))\
            .replace('{{ mask id }}', self.mask_id)

    def __str__(self):
        """Return string representation of badge.

        This will return the badge SVG text.

        Returns: str

        Examples:

            >>> print(Badge('example', '123'))  # doctest: +ELLIPSIS
            <?xml version="1.0" encoding="UTF-8"?>
            ...
        """
        return self.badge_svg_text

    def get_text_width(self, text):
        """Return the width of text.

        Args:
            text(str): Text to get the pixel width of.

        Returns:
            int: Pixel width of the given text based on the badges selected font.

        This implementation assumes a fixed font of:

        font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="11"
        >>> badge = Badge('x', 1, font_name='DejaVu Sans,Verdana,Geneva,sans-serif', font_size=11)
        >>> badge.get_text_width('pylint')
        34
        """
        return _get_approx_string_width(text, self.font_width)

    @property
    def badge_color(self):
        """Badge color based on the configured thresholds.

        Returns: str"""
        # If no thresholds were passed then return the default color
        if not self.thresholds:
            return self.default_color

        if self.value_type == str:
            if self.value in self.thresholds:
                return self.thresholds[self.value]
            else:
                return self.default_color

        # Convert the threshold dictionary into a sorted list of lists
        threshold_list = [[self.value_type(i[0]), i[1]] for i in self.thresholds.items()]
        threshold_list.sort(key=lambda x: x[0])

        color = None

        for threshold, color in threshold_list:
            if float(self.value) < float(threshold):
                return color

        # If we drop out the top of the range then return the last max color
        if color and self.use_max_when_value_exceeds:
            return color
        else:
            return self.default_color

    @property
    def badge_color_code(self):
        """Return the color code for the badge.

        Returns: str

        Raises: ValueError when an invalid badge color is set.
        """
        color = self.badge_color
        if color[0] == '#':
            return color

        try:
            return COLORS[color]
        except KeyError:
            raise ValueError('Invalid color code "%s".  Valid color codes are: %s', (color, ", ".join(COLORS.keys())))

    def write_badge(self, file_path, overwrite=False):
        """Write badge to file."""

        # Validate path (part 1)
        if file_path.endswith('/'):
            raise ValueError('File location may not be a directory.')

        # Get absolute filepath
        path = os.path.abspath(file_path)
        if not path.lower().endswith('.svg'):
            path += '.svg'

        # Validate path (part 2)
        if not overwrite and os.path.exists(path):
            raise RuntimeError('File "{}" already exists.'.format(path))

        with open(path, mode='w') as file_handle:
            file_handle.write(self.badge_svg_text)


# Based on the following SO answer: https://stackoverflow.com/a/16008023/6252525
def _get_approx_string_width(text, font_width, fixed_width=False):
    """
    Get the approximate width of a string using a specific average font width.

    Args:
        text(str): Text string to calculate width of.
        font_width(int): Average width of font characters.
        fixed_width(bool): Indicates that the font is fixed width.

    Returns:
        int: Width of string in pixels.

    Examples:

        Call the function with a string and the maximum character width of the font you are using:

            >>> int(_get_approx_string_width('hello', 10))
            29

        This example shows the comparison of simplistic calculation based on a fixed width.
        Given a test string and a fixed font width of 10, we can calculate the width
        by multiplying the length and the font character with:

            >>> test_string = 'GOOGLE|ijkl'
            >>> _get_approx_string_width(test_string, 10, fixed_width=True)
            110

        Since some characters in the string are thinner than others we expect that the
        apporximate text width will be narrower than the fixed width calculation:

            >>> _get_approx_string_width(test_string, 10)
            77

    """
    if fixed_width:
        return len(text) * font_width

    size = 0.0

    # A dictionary containing percentages that relate to how wide
    # each character will be represented in a variable width font.
    # These percentages can be calculated using the ``_get_character_percentage_dict`` function.
    char_width_percentages = {
        "lij|' ": 40.0,
        '![]fI.,:;/\\t': 50.0,
        '`-(){}r"': 60.0,
        '*^zcsJkvxy': 70.0,
        'aebdhnopqug#$L+<>=?_~FZT0123456789': 70.0,
        'BSPEAKVXY&UwNRCHD': 70.0,
        'QGOMm%W@': 100.0
    }

    for s in text:
        percentage = 100.0
        for k in char_width_percentages.keys():
            if s in k:
                percentage = char_width_percentages[k]
                break
        size += (percentage / 100.0) * float(font_width)

    return int(size)

# This is a helper function that can be used to generate alternate dictionaries
# for the _get_approx_string_width function.  The function is not needed for
# normal operation of this package, and since it depends on the PIL package,
# which is not included in the dependencies the function will remain commented out.
#
# def _get_character_percentage_dict(font_path, font_size):
#     """Get the dictionary used to estimate variable width font text lengths.
#
#     Args:
#         font_path(str): Path to valid font file.
#         font_size(int): Font size to use.
#
#     Returns: dict
#
#     This function can be used to calculate the dictionary used in the
#     ``get_approx_string_width`` function.
#
#     Examples:
#         >>> _get_character_percentage_dict('/Library/Fonts/Verdana.ttf', 9)  # doctest: +ELLIPSIS
#         {"lij|' ": 40, '![]fI.,:;/\\\\t': 50, '`-(){}r"': 60, '*^zcsJkvxy': 70, ...
#     """
#     from PIL import ImageFont
#
#     # List of groups in size order, smallest to largest
#     char_width_groups = [
#         "lij|' ",
#         '![]fI.,:;/\\t',
#         '`-(){}r"',
#         '*^zcsJkvxy',
#         'aebdhnopqug#$L+<>=?_~FZT' + digits,
#         'BSPEAKVXY&UwNRCHD',
#         'QGOMm%W@',
#         ]
#
#     def get_largest_in_group(group):
#         """Get the widest character from the group."""
#         return max([ImageFont.truetype(font_path, font_size).getsize(c)[0] for c in group])
#
#     largest = char_width_groups[-1]
#     font_width = get_largest_in_group(largest)
#     return {group: int((get_largest_in_group(group) / font_width) * 100)
#             for group in char_width_groups}


def parse_args(args):
    """Parse the command line arguments."""
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=textwrap.dedent('''\
Command line utility to generate .svg badges.

This utility can be used to generate .svg badge images, using configurable
thresholds for coloring.  Values can be passed as string, integer or floating
point.  The type will be detected automatically.

Running the utility with a --file option will result in the .svg image being
written to file.  Without the --file option the .svg file content will be
written to stdout, so can be redirected to a file.

Some thresholds have been built in to save time.  To use these thresholds you
can simply specify the template name instead of threshold value/color pairs.

examples:

    Here are some usage specific examples that may save time on defining
    thresholds.

    Pylint
        anybadge.py --value=2.22 --file=pylint.svg pylint

        anybadge.py --label=pylint --value=2.22 --file=pylint.svg \\
          2=red 4=orange 8=yellow 10=green

    Coverage
        anybadge.py --value=65 --file=coverage.svg coverage

        anybadge.py --label=coverage --value=65 --suffix='%%' --file=coverage.svg \\
          50=red 60=orange 80=yellow 100=green

    CI Pipeline
        anybadge.py --label=pipeline --value=passing --file=pipeline.svg \\
          passing=green failing=red

'''))
    parser.add_argument('-l', '--label', type=str, help='The badge label.')
    parser.add_argument('-v', '--value', type=str, help='The badge value.', required=True)
    parser.add_argument('-m', '--value-format', type=str, default=None,
                        help='Formatting string for value (e.g. "%%.2f" for 2dp floats)')
    parser.add_argument('-c', '--color', type=str, help='For fixed color badges use --color'
                                                        'to specify the badge color.',
                        default=DEFAULT_COLOR)
    parser.add_argument('-p', '--prefix', type=str, help='Optional prefix for value.',
                        default='')
    parser.add_argument('-s', '--suffix', type=str, help='Optional suffix for value.',
                        default='')
    parser.add_argument('-d', '--padding', type=int, help='Number of characters to pad on '
                                                          'either side of the badge text.',
                        default=NUM_PADDING_CHARS)
    parser.add_argument('-n', '--font', type=str,
                        help='Font name.  Supported fonts: '
                             ','.join(['"%s"' % x for x in FONT_WIDTHS.keys()]),
                        default=DEFAULT_FONT)
    parser.add_argument('-z', '--font-size', type=int, help='Font size.',
                        default=DEFAULT_FONT_SIZE)
    parser.add_argument('-t', '--template', type=str, help='Location of alternative '
                                                           'template .svg file.',
                        default=TEMPLATE_SVG)
    parser.add_argument('-u', '--use-max', action='store_true',
                        help='Use the maximum threshold color when the value exceeds the '
                             'maximum threshold.')
    parser.add_argument('-f', '--file', type=str, help='Output file location.')
    parser.add_argument('-o', '--overwrite', action='store_true',
                        help='Overwrite output file if it already exists.')
    parser.add_argument('-r', '--text-color', type=str, help='Text color. Single value affects both label'
                                                             'and value colors.  A comma separated pair '
                                                             'affects label and value text respectively.',
                        default=DEFAULT_TEXT_COLOR)
    parser.add_argument('args', nargs=argparse.REMAINDER, help='Pairs of <upper>=<color>. '
                        'For example 2=red 4=orange 6=yellow 8=good. '
                        'Read this as "Less than 2 = red, less than 4 = orange...".')
    return parser.parse_args(args)


def main(args):
    """Generate a badge based on command line arguments."""

    # Args may be sent from command line of as args directly.
    if not args:
        args = sys.argv[1:]

    # Parse command line arguments
    args = parse_args(args)

    label = args.label
    threshold_text = args.args
    suffix = args.suffix

    # Check whether thresholds were sent as one word, and is in the
    # list of templates.  If so, swap in the template.
    if len(args.args) == 1 and args.args[0] in BADGE_TEMPLATES:
        template_name = args.args[0]
        template_dict = BADGE_TEMPLATES[template_name]
        threshold_text = template_dict['threshold'].split(' ')
        if not args.label:
            label = template_dict['label']
        if not args.suffix and 'suffix' in template_dict:
            suffix = template_dict['suffix']

    if not label:
        raise ValueError('Label has not been set.  Please use --label argument.')

    # Create threshold list from args
    threshold_list = [x.split('=') for x in threshold_text]
    threshold_dict = {x[0]: x[1] for x in threshold_list}

    # Create badge object
    badge = Badge(label, args.value, value_prefix=args.prefix, value_suffix=suffix,
                  default_color=args.color, num_padding_chars=args.padding, font_name=args.font,
                  font_size=args.font_size, template=args.template,
                  use_max_when_value_exceeds=args.use_max, thresholds=threshold_dict,
                  value_format=args.value_format, text_color=args.text_color)

    if args.file:
        # Write badge SVG to file
        badge.write_badge(args.file, overwrite=args.overwrite)
    else:
        print(badge.badge_svg_text)


if __name__ == '__main__':
    main()
